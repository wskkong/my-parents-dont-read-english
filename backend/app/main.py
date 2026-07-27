from fastapi import FastAPI
from app.api import briefing        # ← 新增:导入你的路由文件
from app.db import init_db          # ← 新增:启动时建表
from app.api import briefing, pages   # ← 改这行:加上 pages
from app.api import briefing, pages, admin   # 加上 admin
from app.scheduler.jobs import start_scheduler   # ← 顶部加 import
from app.config import settings

app = FastAPI(title="Finance Tool API")

app.include_router(admin.router)             # 新增这行
app.include_router(briefing.router)  # ← 新增:把 briefing 的端点接进来
app.include_router(briefing.router)
app.include_router(pages.router)      # ← 新增这行

@app.on_event("startup")             # ← 新增:程序启动时自动建表
def on_startup():
    init_db()
    if settings.enable_scheduler:        # ← 只有开关打开才启动
        start_scheduler()
    else:
        print("[scheduler] 已禁用(本地开发)")


@app.get("/health")
def health():
    return {"status": "ok"}
