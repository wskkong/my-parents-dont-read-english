from apscheduler.schedulers.background import BackgroundScheduler
from app.config import settings
from app.processing.briefing_service import run_briefing, has_todays_briefing

scheduler = BackgroundScheduler(timezone=settings.timezone)


def scheduled_job():
    """定时任务:到点跑简报"""
    print("[scheduler] 06:00 触发,开始生成简报")
    run_briefing()


def start_scheduler():
    """启动调度器 + 开机补跑"""
    # 1. 注册每天 06:00 的任务
    scheduler.add_job(scheduled_job, "cron", hour=6, minute=0)
    scheduler.start()

    # 2. 开机补跑:今天没生成就补一次
    if not has_todays_briefing():
        print("[scheduler] 今天还没有简报,补跑一次")
        run_briefing()
    else:
        print("[scheduler] 今天已有简报,跳过补跑")