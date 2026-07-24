from sqlmodel import SQLModel, create_engine, Session
from app.config import settings
from app.models.briefing import Briefing  # 导入蓝图,create_all 才知道要建哪些表

# 1. 创建"引擎"——连接到数据库文件
engine = create_engine(settings.database_url, echo=True)


# 2. 建表:根据所有 SQLModel 蓝图,在数据库里创建对应的表
def init_db():
    SQLModel.metadata.create_all(engine)


# 3. 提供数据库会话(以后存/取数据时用)
def get_session():
    return Session(engine)