from fastapi import APIRouter, HTTPException, Header
from app.processing.briefing_service import run_briefing
from app.config import settings

router = APIRouter()


@router.post("/admin/run-briefing")
def trigger_briefing(x_admin_token: str = Header(None)):
    if x_admin_token != settings.admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return run_briefing()