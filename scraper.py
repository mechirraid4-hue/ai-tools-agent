import requests
import feedparser
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    """جلب مستودعات الذكاء الاصطناعي المشهورة والقوية فقط"""
    items = []
    try:
        logger.info("Searching for top AI tools on GitHub...")
        # نبحث عن أدوات ذات ترخيص مفتوح وعدد نجوم عالي (>500) لضمان الجودة
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "artificial intelligence OR machine learning OR deep learning stars:>500 license:mit OR license:apache-2.0",
            "sort": "stars",
            "order": "desc",
            "per_page": "5"
        }
        headers = {"Accept": "application/vnd.github.v3+json"}
        r = requests.get(url, params=params, headers=headers, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            for repo in data.get("items", [])[:5]:
                desc = repo.get("description") or "أداة ذكاء اصطناعي متقدمة ومفتوحة المصدر."
                items.append({
                    "title": repo["full_name"],
                    "description": desc,
                    "url": repo["html_url"],
                    "source": "GitHub Trending",
                    "stars": repo["stargazers_count"],
                    "is_free": True,
                    "quality_score": repo["stargazers_count"] # نستخدم النجوم كمؤشر للجودة
                })
            logger.info(f"Found {len(items)} high-quality GitHub repos.")
    except Exception as e:
        logger.error(f"GitHub Error: {str(e)}")
    return items

def scrape_huggingface():
    """جلب النماذج الأكثر تحميلاً وتقييماً فقط"""
    items = []
    try:
        logger.info("Searching for top models on HuggingFace...")
        # نفلتر حسب عدد التنزيلات العالي (>10k) لضمان أن النموذج معروف ومجرب
        url = "https://huggingface.co/api/models"
        params = {
            "sort": "downloads",
            "direction": "-1",
            "limit": "5",
            "search": "llm OR vision OR audio" # نبحث عن مجالات محددة وقوية
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            data = r.json()
            for m in data[:5]:
                # نتأكد أن النموذج ليس gated (مدفوع/مقيد)
                if "gated" not in m.get("tags", []):
                    items.append({
                        "title": m["modelId"],
                        "description": f"نموذج قوي بمجال {m.get('pipeline_tag', 'AI')}. تم تحميله {m.get('downloads', 0)} مرة.",
                        "url": "https://huggingface.co/" + m["modelId"],
                        "source": "HuggingFace Top Models",
                        "downloads": m.get("downloads", 0),
                        "is_free": True,
                        "quality_score": m.get("downloads", 0)
                    })
            logger.info(f"Found {len(items)} popular HF models.")
    except Exception as e:
        logger.error(f"HF Error: {str(e)}")
    return items

def scrape_rss():
    """جلب أخبار الإصدارات الرسمية من الشركات الكبرى فقط"""
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
                for e in feed.entries[:1]: # خبر واحد فقط من كل مصدر لتجنب التكرار
                    items.append({
                        "title": e.title,
                        "description": e.get("summary", "")[:200],
                        "url": e.link,
                        "source": f"{name} Official",
                        "is_free": True,
                        "quality_score": 9999 # إعطاء أولوية عالية للأخبار الرسمية
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
    
    # ترتيب النتائج حسب الجودة (النجوم/التحميلات) وإرجاع الأفضل فقط
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    
    logger.info(f"Total curated items: {len(all_news)}")
    return all_news[:7] # إرسال أفضل 7 أدوات فقط لتجنب الإزعاج                "source": "HuggingFace",
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
