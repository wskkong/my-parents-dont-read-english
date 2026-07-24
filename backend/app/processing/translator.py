from app.services.llm_client import generate


def translate_to_chinese(english_text):
    prompt = f"""Translate the following financial briefing into Chinese. 
    Keep it complete and professional. Keep key financial/technical terms 
    in English where appropriate (e.g. ETF, AI, GDP).

    English briefing:
    {english_text}

    中文翻译:"""

    return generate(prompt)