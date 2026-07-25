import feedparser

def fetch_news(url):
    try:
        feed = feedparser.parse(url)
        source = feed.feed.get("title", "Unknown")   # ← 整个源的名字
        articles = []
        for entry in feed.entries:
            article = {
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "source": source,                     # ← 新增:真实来源
            }
            articles.append(article)
        return articles
    except Exception as e:
            print(f"[news_fetcher] 抓取失败 {url}: {e}")
            return []

def fetch_all_news(urls, per_source=5):
    all_articles = []
    for url in urls:
        try:
            articles = fetch_news(url)
            all_articles += articles[:per_source]    # ← 每个源只取前 N 条
        except Exception as e:
            print(f"[fetch_all_news] 跳过失败的源 {url}: {e}")
    return all_articles