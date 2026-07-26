from sqlmodel import SQLModel, create_engine, Session
from app.config import settings
from app.models.briefing import Briefing  # 导入蓝图,create_all 才知道要建哪些表

# Railway 给的是 postgresql://,但我们用的驱动是 psycopg v3,
# 需要把它改成 postgresql+psycopg:// 让 SQLAlchemy 用对驱动
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+psycopg://", 1)


# SQLite 需要 check_same_thread=False;Postgres 不需要
connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}

# 1. 创建"引擎"——连接到数据库文件
engine = create_engine(settings.database_url, echo=False, connect_args=connect_args)


# 2. 建表:根据所有 SQLModel 蓝图,在数据库里创建对应的表
def init_db():
    SQLModel.metadata.create_all(engine)


# 3. 提供数据库会话(以后存/取数据时用)
def get_session():
    return Session(engine)