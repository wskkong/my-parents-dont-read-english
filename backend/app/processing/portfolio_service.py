from sqlmodel import select
from app.db import get_session
from app.models.transaction import Transaction, Dividend
import pandas as pd
from datetime import datetime

def import_activity_csv(file_path):
    # CSV 前 8 行是导出说明,真正表头在第 8 行(0-indexed),所以 skiprows=8
    df = pd.read_csv(file_path, skiprows=8)

    imported = 0
    skipped = 0

    for _, row in df.iterrows():
        activity = str(row["Activity"]).strip()

        # 只处理 Buy / Sell,其他类型跳过
        if activity == "Buy":
            action = "buy"
        elif activity == "Sell":
            action = "sell"
        elif activity in ("Dividends", "Distribution"):
            # 股息:存进 dividend 表,不当交易
            trade_date = datetime.strptime(str(row["Date"]).strip(), "%B %d, %Y").date()
            add_dividend(
                symbol=str(row["Symbol"]).strip(),
                amount=abs(float(row["Value"])),        # 金额用 Value 列,取绝对值
                pay_date=trade_date,
                currency=str(row["Currency"]).strip(),
                account=str(row["Account"]).strip(),
                div_type=activity.lower(),               # "dividends" 或 "distribution"
            )
            imported += 1
            continue                                     # 处理完跳到下一行
        else:
            skipped += 1
            continue

        # 解析日期(RBC 格式如 "July 7, 2026")
        trade_date = datetime.strptime(str(row["Date"]).strip(), "%B %d, %Y").date()

        add_transaction(
            symbol=str(row["Symbol"]).strip(),
            action=action,
            price=abs(float(row["Price"])),
            quantity=abs(float(row["Quantity"])),
            trade_date=trade_date,
            currency=str(row["Currency"]).strip(),
            account=str(row["Account"]).strip(),
        )
        imported += 1

    return {"imported": imported, "skipped": skipped}

def calculate_cost(symbol, account):
    with get_session() as session:
        # 读出这只股票在这个账户的所有交易,按日期排序
        statement = (
            select(Transaction)
            .where(Transaction.symbol == symbol)
            .where(Transaction.account == account)
            .order_by(Transaction.trade_date)      # 按时间顺序,关键
        )
        transactions = session.exec(statement).all()

    shares = 0.0          # 剩余股数
    cost = 0.0            # 每股平均成本(ACB)
    realized_gain = 0.0   # 已实现盈亏(卖出赚/亏的,税务要用)

    for tx in transactions:
        if tx.action == "buy":
            # 买入:成本只由买入决定(ACB 平均法)
            total_cost = cost * shares + tx.price * tx.quantity
            shares = shares + tx.quantity
            cost = total_cost / shares if shares > 0 else 0.0
        elif tx.action == "sell":
            # 卖出:每股成本不变;记录已实现盈亏
            realized_gain += (tx.price - cost) * tx.quantity
            shares = shares - tx.quantity

    return {
        "symbol": symbol,
        "account": account,
        "shares": shares,
        "cost": round(cost, 4),
        "realized_gain": round(realized_gain, 2),
    }

def add_transaction(symbol, action, price, quantity, trade_date, currency="CAD", account=""):
    tx = Transaction(
        symbol=symbol,
        action=action,
        price=price,
        quantity=quantity,
        trade_date=trade_date,
        currency=currency,
        account=account,
    )
    with get_session() as session:
        session.add(tx)
        session.commit()
    return {"status": "added", "symbol": symbol}

def add_dividend(symbol, amount, pay_date, currency="CAD", account="", div_type="dividend"):
    div = Dividend(
        symbol=symbol,
        amount=amount,
        pay_date=pay_date,
        currency=currency,
        account=account,
        div_type=div_type,
    )
    with get_session() as session:
        session.add(div)
        session.commit()
    return {"status": "added", "symbol": symbol}