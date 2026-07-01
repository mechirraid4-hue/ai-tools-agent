import requests
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

def scrape_github_trending():
    """جلب أدوات GitHub الرائدة حديثاً (مرونة عالية)"""
    items = []
    try:
        logger.info("Searching GitHub for rising AI tools...")
        # معايير مرنة: تركيز على التحديث الأخير والنشاط بدلاً من النجوم فقط
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "topic:artificial-intelligence OR topic:llm OR topic:rag pushed:>2024-06-01",
            "sort": "updated",
            "order": "desc",
            "per_page": "8"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            for repo in r.json().get("items", [])[:8]:
                # قبول أي أداة لها وصف واضح ونشاط حديث
                if repo.get("description") and repo.get("pushed_at"):
                    # حساب تاريخ آخر تحديث
                    last_push = datetime.fromisoformat(repo['pushed_at'].replace('Z', '+00:00'))
                    if (datetime.now(timezone.utc) - last_push) < timedelta(days=14):
                        items.append({
                            "title": repo["full_name"],
                            "description": repo["description"],
                            "url": repo["html_url"],
                            "source": "GitHub Rising",
                            "stars": repo["stargazers_count"],
                            "is_free": True,
                            "quality_score": repo["stargazers_count"] + 500  # دفعة للنشاط الحديث
                        })
        logger.info(f"Found {len(items)} rising GitHub tools.")
    except Exception as e:
        logger.error(f"GitHub Trending Error: {str(e)}")
    return items

def scrape_huggingface_trending():
    """جلب نماذج HuggingFace الصاعدة"""
    items = []
    try:
        logger.info("Searching HuggingFace for trending models...")
        url = "https://huggingface.co/api/models"
        params = {
            "sort": "likes",  # التركيز على الإعجابات الحديثة
            "direction": "-1",
            "limit": "6",
            "search": "llm OR vision OR agent"
        }
        r = requests.get(url, params=params, timeout=15)
        
        if r.status_code == 200:
            for m in r.json()[:6]:
                if "gated" not in m.get("tags", []):
                    items.append({
                        "title": m["modelId"],
                        "description": f"نموذج {m.get('pipeline_tag', 'AI')} صاعد بسرعة.",
                        "url": "https://huggingface.co/" + m["modelId"],
                        "source": "HuggingFace Trending",
                        "downloads": m.get("downloads", 0),
                        "is_free": True,
                        "quality_score": m.get("likes", 0) * 10
                    })
        logger.info(f"Found {len(items)} trending HF models.")
    except Exception as e:
        logger.error(f"HF Trending Error: {str(e)}")
    return items

def scrape_producthunt_ai():
    """جلب أدوات الذكاء الاصطناعي من ProductHunt (أدوات غير GitHub)"""
    items = []
    try:
        logger.info("Checking ProductHunt AI tools...")
        # RSS عام لـ ProductHunt مع فلتر AI يدوي لاحقاً
        feed_url = "https://www.producthunt.com/feed"
        r = requests.get(feed_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        
        if r.status_code == 200:
            # تحليل بسيط لـ XML (بدون مكتبات ثقيلة)
            import xml.etree.ElementTree as ET
            root = ET.fromstring(r.content)
            for item in root.findall(".//item")[:5]:
                title = item.find("title").text
                desc = item.find("description").text
                link = item.find("link").text
                # فلتر سريع: نأخذ فقط ما يحتوي على AI أو Tool أو App
                if any(kw in title.lower() for kw in ["ai", "tool", "app", "agent", "llm"]):
                    items.append({
                        "title": title,
                        "description": desc[:300],
                        "url": link,
                        "source": "ProductHunt AI",
                        "is_free": True,
                        "quality_score": 700  # أولوية متوسطة للأدوات الجديدة
                    })
        logger.info(f"Found {len(items)} ProductHunt AI tools.")
    except Exception as e:
        logger.error(f"ProductHunt Error: {str(e)}")
    return items

def scrape_all_sources():
    all_news = []
    # دمج المصادر المتنوعة
    all_news.extend(scrape_producthunt_ai())   # أدوات جديدة غير GitHub
    all_news.extend(scrape_github_trending())  # مستودعات صاعدة
    all_news.extend(scrape_huggingface_trending()) # نماذج رائجة
    
    # ترتيب حسب الجودة مع تنويع المصادر
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    
    # أخذ أفضل 5 أدوات من مصادر مختلفة
    final_items = []
    seen_sources = set()
    for item in all_news:
        src = item.get("source", "")
        if src not in seen_sources or len(final_items) < 5:
            final_items.append(item)
            seen_sources.add(src)
        if len(final_items) >= 5:
            break
            
    logger.info(f"Selected {len(final_items)} diverse trending tools.")
    return final_items
