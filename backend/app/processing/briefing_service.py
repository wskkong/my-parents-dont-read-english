from app.db import get_session
from app.models.briefing import Briefing
from sqlmodel import select

def save_briefing(date, level, lang, content):
    briefing = Briefing(date=date, level=level, lang=lang, content=content)  # 1. 造一条记录
    with get_session() as session:      # 2. 打开一次数据库会话
        session.add(briefing)           #    把记录加进去
        session.commit()                #    提交(真正写入硬盘)

def get_latest_briefing(lang):
    with get_session() as session:
        statement = (
            select(Briefing)
            .where(Briefing.lang == lang)
            .order_by(Briefing.generated_at.desc())
        )
        return session.exec(statement).first()