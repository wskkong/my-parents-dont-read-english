from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import date
from app.processing.portfolio_service import add_transaction

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


# 显示录入表单
@router.get("/portfolio/add", response_class=HTMLResponse)
def add_form(request: Request):
    return templates.TemplateResponse(request, "add_transaction.html", {})


# 接收表单提交
@router.post("/portfolio/add")
def add_submit(
    symbol: str = Form(...),
    action: str = Form(...),
    price: float = Form(...),
    quantity: float = Form(...),
    trade_date: date = Form(...),
    currency: str = Form("CAD"),
    account: str = Form(""),
):
    add_transaction(symbol, action, price, quantity, trade_date, currency, account)
    return RedirectResponse(url="/portfolio/add", status_code=303)