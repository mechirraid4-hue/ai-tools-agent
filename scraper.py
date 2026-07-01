import requests
import feedparser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def scrape_github():
    """جلب أدوات GitHub الحديثة والقوية (Trending)"""
    items = []
    try:
        logger.info("Searching for Trending AI tools on GitHub...")
        # نبحث عن أدوات ذكاء اصطناعي مفتوحة المصدر، مرتبة حسب التحديث الأخير
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "artificial intelligence OR machine learning OR deep learning license:mit OR license:apache-2.0 created:>2024-01-01",
            "sort": "updated",  # التركيز على الحديث بدلاً من النجوم فقط
            "order": "desc",
            "per_page": "5"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            for repo in data.get("items", [])[:5]:
                # شرط الجودة: يجب أن يكون له وصف وعدد نجوم معقول (>50)
                if repo.get("description") and repo["stargazers_count"] > 50:
                    items.append({
                        "title": repo["full_name"],
                        "description": repo["description"],
                        "url": repo["html_url"],
                        "source": "GitHub Trending",
                        "stars": repo["stargazers_count"],
                        "is_free": True,
                        "quality_score": repo["stargazers_count"] + 1000  # وزن إضافي للتحديث
                    })
            logger.info(f"Found {len(items)} trending GitHub repos.")
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
            "sort": "lastModified",  # الترتيب حسب آخر تحديث وليس التحميلات
            "direction": "-1",
            "limit": "10",
            "search": "llm OR vision OR audio OR embedding"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            count = 0
            for m in data:
                if count >= 5: break
                # استبعاد النماذج المقيدة (Gated) والتأكد من وجود وصف
                if "gated" not in m.get("tags", []) and m.get("cardData", {}).get("license"):
                    items.append({
                        "title": m["modelId"],
                        "description": f"نموذج {m.get('pipeline_tag', 'AI')} مجاني ومحدث.",
                        "url": "https://huggingface.co/" + m["modelId"],
                        "source": "HuggingFace Recent",
                        "downloads": m.get("downloads", 0),
                        "is_free": True,
                        "quality_score": 500  # وزن ثابت للأدوات الحديثة
                    })
                    count += 1
            logger.info(f"Found {len(items)} recent HF models.")
    except Exception as e:
        logger.error(f"HF Error: {str(e)}")
    return items

def scrape_rss():
    """جلب أخبار الإصدارات الرسمية الجديدة"""
    items = []
    try:
        logger.info("Checking official AI blogs...")
        feeds = [
            ("OpenAI", "https://openai.com/blog/rss.xml"),
            ("Google AI", "https://blog.google/technology/ai/rss/"),
            ("Meta AI", "https://ai.meta.com/blog/rss/")
        ]
        for name, url in feeds:
            try:
                feed = feedparser.parse(url)
                for e in feed.entries[:1]:
                    items.append({
                        "title": e.title,
                        "description": e.get("summary", "")[:200],
                        "url": e.link,
                        "source": f"{name} Official",
                        "is_free": True,
                        "quality_score": 2000  # أولوية عالية للأخبار الرسمية
                    })
            except:
                pass
        logger.info(f"Found {len(items)} official announcements.")
    except Exception as e:
        logger.error(f"RSS Error: {str(e)}")
    return items

def scrape_all_sources():
    all_news = []
    all_news.extend(scrape_github())
    all_news.extend(scrape_huggingface())
    all_news.extend(scrape_rss())
    
    # خلط النتائج قليلاً لضمان التنوع، ثم ترتيبها
    # نأخذ أفضل 5 أدوات متنوعة
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    
    final_items = all_news[:5] 
    
    logger.info(f"Selected {len(final_items)} diverse tools for this run.")
    return final_items
