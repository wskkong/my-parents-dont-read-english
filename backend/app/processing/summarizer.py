from app.services.llm_client import generate

def summarize_news(articles):
    news_text = ""
    for article in articles:
        news_text += f"标题: {article['title']}\n摘要: {article['summary']}\n来源: {article['source']}\n\n"
    prompt = f"""You are a financial news analyst. Provide a summary of the most important geopolitical events happening today that will impact the stock and global trade markets. 
Only pick geopolitical news with great impact on the technology / AI / energy stock market, as well as economic impact on Canada, US, Japan and China. 
Add a disclaimer at the top: "This content is AI-generated." The news comes from multiple sources and may cover the same event. 
Draw on the different perspectives (geopolitical, financial, tech) across sources to give a fuller picture.
Merge duplicate stories and cite all relevant sources.
Write the entire briefing in English. For each story, cite its source at the end (the source is provided in the news data below) Make sure source is display in format as BBC News.

News:
{news_text}

Briefing:"""
    return generate(prompt)

