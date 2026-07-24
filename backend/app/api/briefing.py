from fastapi import APIRouter
from app.processing.briefing_service import get_latest_briefing

router = APIRouter()


@router.get("/briefing/latest")
def read_latest(lang: str = "EN"):
    briefing = get_latest_briefing(lang)
    if briefing is None:
        return {"error": "还没有简报"}
    return briefing