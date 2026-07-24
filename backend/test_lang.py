from app.processing.briefing_service import get_latest_briefing

en = get_latest_briefing("EN")
zh = get_latest_briefing("ZH")

print("EN:", en.content if en else "没有")
print("ZH:", zh.content if zh else "没有")