import requests
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    """جلب أدوات GitHub الحديثة والقوية فقط"""
    items = []
    try:
        logger.info("Searching for Trending AI tools on GitHub...")
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "artificial intelligence OR machine learning license:mit OR license:apache-2.0 stars:>50",
            "sort": "updated",
            "order": "desc",
            "per_page": "3"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            for repo in data.get("items", [])[:3]:
                if repo.get("description"):
                    items.append({
                        "title": repo["full_name"],
                        "description": repo["description"],
                        "url": repo["html_url"],
                        "source": "GitHub Trending",
                        "stars": repo["stargazers_count"],
                        "is_free": True,
                        "quality_score": repo["stargazers_count"]
                    })
    except Exception as e:
        logger.error(f"GitHub Error: {str(e)}")
    return items

def scrape_huggingface():
    """جلب نماذج Hugging Face الحديثة والمجانية"""
    items = []
    try:
        logger.info("Searching for recent HF models...")
        url = "https://huggingface.co/api/models"
        params = {
            "sort": "lastModified",
            "direction": "-1",
            "limit": "5",
            "search": "llm OR vision OR audio"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            count = 0
            for m in data:
                if count >= 3: break
                if "gated" not in m.get("tags", []):
                    items.append({
                        "title": m["modelId"],
                        "description": f"نموذج {m.get('pipeline_tag', 'AI')} مجاني ومحدث.",
                        "url": "https://huggingface.co/" + m["modelId"],
                        "source": "HuggingFace Recent",
                        "downloads": m.get("downloads", 0),
                        "is_free": True,
                        "quality_score": m.get("downloads", 0)
                    })
                    count += 1
    except Exception as e:
        logger.error(f"HF Error: {str(e)}")
    return items

def scrape_all_sources():
    all_news = []
    # حذفنا RSS تماماً لضمان عدم إرسال أخبار ومقالات
    all_news.extend(scrape_github())
    all_news.extend(scrape_huggingface())
    
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    final_items = all_news[:4] 
    
    logger.info(f"Selected {len(final_items)} diverse tools.")
    return final_items
