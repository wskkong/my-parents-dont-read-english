from fastapi import FastAPI
from app.api import briefing        # ← 新增:导入你的路由文件
from app.db import init_db          # ← 新增:启动时建表

app = FastAPI(title="Finance Tool API")

app.include_router(briefing.router)  # ← 新增:把 briefing 的端点接进来


@app.on_event("startup")             # ← 新增:程序启动时自动建表
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}