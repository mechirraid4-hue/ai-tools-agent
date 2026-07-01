import requests
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    items = []
    try:
        logger.info("Fetching GitHub AI tools...")
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "artificial intelligence stars:>100",
            "sort": "stars",
            "order": "desc",
            "per_page": "3"
        }
        headers = {"Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        if r.status_code == 200:
            repos = r.json().get("items", [])
            logger.info(f"GitHub API returned {len(repos)} repos")
            
            for repo in repos[:3]:
                items.append({
                    "title": repo["full_name"],
                    "description": repo.get("description", "AI Tool"),
                    "url": repo["html_url"],
                    "source": "GitHub",
                    "stars": repo["stargazers_count"],
                    "is_free": True,
                    "quality_score": repo["stargazers_count"]
                })
                logger.info(f"Added: {repo['full_name']} ({repo['stargazers_count']} stars)")
    except Exception as e:
        logger.error(f"GitHub Error: {str(e)}")
    return items

def scrape_huggingface():
    items = []
    try:
        logger.info("Fetching HuggingFace models...")
        url = "https://huggingface.co/api/models"
        params = {
            "sort": "downloads",
            "direction": "-1",
            "limit": "3"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            models = r.json()
            logger.info(f"HF API returned {len(models)} models")
            
            for m in models[:3]:
                items.append({
                    "title": m["modelId"],
                    "description": f"Model with {m.get('downloads', 0)} downloads",
                    "url": "https://huggingface.co/" + m["modelId"],
                    "source": "HuggingFace",
                    "downloads": m.get("downloads", 0),
                    "is_free": True,
                    "quality_score": m.get("downloads", 0)
                })
                logger.info(f"Added: {m['modelId']}")
    except Exception as e:
        logger.error(f"HF Error: {str(e)}")
    return items

def scrape_all_sources():
    all_news = []
    all_news.extend(scrape_github())
    all_news.extend(scrape_huggingface())
    
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    
    logger.info(f"Total items before filtering: {len(all_news)}")
    return all_news[:4]
