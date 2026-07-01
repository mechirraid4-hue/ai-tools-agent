import requests
import feedparser
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    items = []
    try:
        url = "https://api.github.com/search/repositories"
        params = {"q": "ai license:mit", "sort": "stars", "per_page": "3"}
        r = requests.get(url, params=params, timeout=10)
        for repo in r.json().get("items", [])[:3]:
            if repo.get("description"):
                items.append({
                    "title": repo["full_name"],
                    "description": repo["description"],
                    "url": repo["html_url"],
                    "source": "GitHub",
                    "is_free": True
                })
    except:
        pass
    return items

def scrape_hf():
    items = []
    try:
        url = "https://huggingface.co/api/models"
        params = {"sort": "lastModified", "limit": "3"}
        r = requests.get(url, params=params, timeout=10)
        for m in r.json()[:3]:
            items.append({
                "title": m["modelId"],
                "description": "Free model",
                "url": "https://huggingface.co/" + m["modelId"],
                "source": "HuggingFace",
                "is_free": True
            })
    except:
        pass
    return items

def scrape_rss():
    items = []
    try:
        feed = feedparser.parse("https://openai.com/blog/rss.xml")
        for e in feed.entries[:2]:
            items.append({
                "title": e.title,
                "description": e.get("summary", "")[:100],
                "url": e.link,
                "source": "OpenAI",
                "is_free": True
            })
    except:
        pass
    return items

def scrape_all_sources():
    all_news = []
    all_news.extend(scrape_github())
    all_news.extend(scrape_hf())
    all_news.extend(scrape_rss())
    logger.info("Total: " + str(len(all_news)))
    return all_news
