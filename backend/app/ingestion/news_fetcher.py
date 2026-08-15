import feedparser

def fetch_news(url, name): 
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            article = {
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "source": name,                     # ← 新增:真实来源
            }
            articles.append(article)
        return articles
    except Exception as e:
            print(f"[news_fetcher] 抓取失败 {url}: {e}")
            return []

def fetch_all_news(sources, per_source=5):
    all_articles = []
    for url, name in sources.items():
        try:
            articles = fetch_news(url, name)
            all_articles += articles[:per_source]    # ← 每个源只取前 N 条
        except Exception as e:
            print(f"[fetch_all_news] 跳过失败的源 {url}: {e}")
    return all_articles