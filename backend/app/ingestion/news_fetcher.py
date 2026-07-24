import feedparser

def fetch_news(url):
    feed = feedparser.parse(url) #feedparser.parser is a library that parses RSS feeds and returns a structured object containing the feed's metadata and entries. 

    articles = [ ]
    for entry in feed.entries: #feed.entries is a list of entries in the feed, where each entry is a dictionary containing the entry's metadata and content.
        article = {
            "title":entry.title, #entry.title is the title of the entry.
            "link": entry.link, #entry.link is the link to the entry.
            "summary": entry.summary, #entry.summary is the summary of the entry.
        }
        articles.append(article) #append the article to the articles list.
    return articles #return the articles list.

