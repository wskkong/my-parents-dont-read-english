from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.processing.briefing_service import get_latest_briefing, get_all_briefings, get_briefing_by_id

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
    
@router.get("/archive", response_class=HTMLResponse)
def archive(request: Request, lang: str = "EN"):
    briefings = get_all_briefings(lang)
    return templates.TemplateResponse(
        request,
        "archive.html",
        {"briefings": briefings, "lang": lang},
    )

@router.get("/briefing/{briefing_id}", response_class=HTMLResponse)
def view_briefing(request: Request, briefing_id: int):
    briefing = get_briefing_by_id(briefing_id)
    return templates.TemplateResponse(
        request,
        "dashboard.html",
        {"briefing": briefing, "lang": briefing.lang if briefing else "EN"},
    )