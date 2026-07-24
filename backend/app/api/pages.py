from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.processing.briefing_service import get_latest_briefing

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request, lang: str = "EN"):
    briefing = get_latest_briefing(lang)
    return templates.TemplateResponse(
        request,                                          # ← request 作为第一个参数
        "dashboard.html",                                 # ← 模板名第二个
        {"briefing": briefing, "lang": lang},             # ← 数据里不用再放 request
    )