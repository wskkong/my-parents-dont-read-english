from app.db import init_db
from app.processing.briefing_service import save_briefing

init_db()
save_briefing("2026-07-24", "International", "EN", "This is a test briefing.")
save_briefing("2026-07-24", "International", "ZH", "这是一条测试简报。")
print("已存入两条")