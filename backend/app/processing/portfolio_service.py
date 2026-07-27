from sqlmodel import select
from app.db import get_session
from app.models.transaction import Transaction


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