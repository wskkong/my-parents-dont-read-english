from sqlmodel import SQLModel, Field
from datetime import date as date_type


class Transaction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str                     # 股票代码(NVDA)
    action: str                     # buy 买入 / sell 卖出 / drip 分红再投 
    price: float                    # 成交单价
    price: float                    # 成交单价(drip: 再投时的买入价)
    quantity: float                 # 数量(drip: 再投买入的股数)
    trade_date: date_type
    currency: str = "CAD"           # 币种(默认 CAD,美股改 USD)
    account: str = ""               # 账户(TFSA 等)
    
class StockSplit(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str                     # 哪只股票拆分
    split_date: date_type           # 拆分日期
    ratio_from: float               # 拆分前(如 1)
    ratio_to: float                 # 拆分后(如 4)= 1拆4
    account: str = ""
    
class Dividend(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    symbol: str                     # 哪只股票的股息
    amount: float                   # 股息金额(现金)
    pay_date: date_type             # 派息日期
    currency: str = "CAD"           # 币种
    account: str = ""               # 账户
    div_type: str = "dividend"      # 类型:dividend / distribution(REIT分配)