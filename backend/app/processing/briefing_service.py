from app.db import get_session
from app.models.briefing import Briefing
from sqlmodel import select
from app.processing.summarizer import summarize_news
from app.processing.translator import translate_to_chinese
from app.ingestion.news_fetcher import fetch_news, fetch_all_news
from app.ingestion.sources import NEWS_SOURCES
from datetime import datetime
from zoneinfo import ZoneInfo
from app.config import settings

def today_str():
    """按配置的时区(America/Vancouver)返回今天的日期字符串"""
    return str(datetime.now(ZoneInfo(settings.timezone)).date())


def save_briefing(date, level, lang, content,sources=""):
    briefing = Briefing(date=date, level=level, lang=lang, content=content, sources=sources)  # 1. 造一条记录
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
    
def get_all_briefings(lang):
    with get_session() as session:
        statement = (
            select(Briefing)
            .where(Briefing.lang == lang)
            .order_by(Briefing.generated_at.desc())
        )
        return session.exec(statement).all()
    

def run_briefing():
    try:
        # 1. 抓新闻
        news = fetch_all_news(NEWS_SOURCES, per_source=5)
       
        # 防御:如果没抓到任何新闻,别往下走
        if not news:
            return {"status": "error", "message": "没有抓到新闻"}
        
        selected = news    # 已经每源限量了,直接用

        # 2. 生成英文简报
        english = summarize_news(selected)

        # 3. 翻译成中文
        chinese = translate_to_chinese(english)

        # 收集来源清单:每条 "标题|||链接",用换行分隔
        sources = "\n".join(f"{a['title']}|||{a['link']}" for a in selected)

        # 4. 分别存进数据库(两条独立记录)
        today = today_str()          # ← 原来是 str(date_type.today())
        save_briefing(today, "International", "EN", english, sources)
        save_briefing(today, "International", "ZH", chinese, sources)

        return {"status": "done"}
    
    except Exception as e:
        print(f"[run_briefing] 生成失败: {e}")
        return {"status": "error", "message": "简报生成失败,请稍后再试"}

def has_todays_briefing():
    today = today_str()          # ← 原来是 str(date_type.today())
    with get_session() as session:
        statement = select(Briefing).where(Briefing.date == today, Briefing.lang == "ZH")  # 只要ZH有就算今天已经生成了
        result = session.exec(statement).first()
        return result is not None # 查到了 = True,没查到 = False
    
def get_briefing_by_id(briefing_id):
    with get_session() as session:
        return session.get(Briefing, briefing_id)

def delete_briefing_by_id(briefing_id):
    with get_session() as session:
        briefing = session.get(Briefing, briefing_id)
        if briefing is None:
            return {"status": "not found", "id": briefing_id}
        session.delete(briefing)
        session.commit()
        return {"status": "deleted", "id": briefing_id}
