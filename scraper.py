import requests
import feedparser
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    items = []
    try:
        url = "https://api.github.com/search/repositories"
        params = {"q": "ai stars:>100 license:mit", "sort": "stars", "per_page": "3"}
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            for repo in r.json().get("items", [])[:3]:
                items.append({
                    "title": repo["full_name"],
                    "description": repo.get("description", "AI Tool"),
                    "url": repo["html_url"],
                    "source": "GitHub",
                    "stars": repo["stargazers_count"],
                    "is_free": True,
                    "quality_score": repo["stargazers_count"]
                })
    except Exception as e:
        logger.error(str(e))
    return items

def scrape_huggingface():
    items = []
    try:
        url = "https://huggingface.co/api/models"
        params = {"sort": "downloads", "limit": "3"}
        r = requests.get(url, params=params, timeout=15)
        if r.status_code == 200:
            for m in r.json()[:3]:
                if "gated" not in m.get("tags", []):
                    items.append({
                        "title": m["modelId"],
                        "description": "Free AI Model",
                        "url": "https://huggingface.co/" + m["modelId"],
                        "source": "HuggingFace",
                        "downloads": m.get("downloads", 0),
                        "is_free": True,
                        "quality_score": m.get("downloads", 0)
                    })
    except Exception as e:
        logger.error(str(e))
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
                "is_free": True,
                "quality_score": 9999
            })
    except Exception as e:
        logger.error(str(e))
    return items

def scrape_all_sources():
    all_news = []
    all_news.extend(scrape_github())
    all_news.extend(scrape_huggingface())
    all_news.extend(scrape_rss())
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    return all_news[:3]
