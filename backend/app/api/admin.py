from fastapi import APIRouter
from app.processing.briefing_service import run_briefing

router = APIRouter()


@router.post("/admin/run-briefing")
def trigger_briefing():
    return run_briefing()