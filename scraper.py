import requests
import logging

logger = logging.getLogger(__name__)

def scrape_github():
    """جلب أدوات GitHub الحديثة والقوية"""
    items = []
    try:
        logger.info("Searching for Trending AI tools on GitHub...")
        # بحث شامل عن أدوات الذكاء الاصطناعي والتطوير
        url = "https://api.github.com/search/repositories"
        params = {
            "q": "artificial intelligence OR machine learning OR deep-learning license:mit OR license:apache-2.0 stars:>100",
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
    """جلب نماذج Hugging Face الحديثة"""
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

def scrape_design_tools():
    """جلب أدوات تصميم الواجهات والمواقع المدعومة بالذكاء الاصطناعي"""
    items = []
    try:
        logger.info("Searching for AI Design & UI tools...")
        # كلمات مفتاحية للبحث عن أدوات التصميم
        design_queries = [
            "ai-ui-generator", 
            "figma-plugin-ai", 
            "website-builder-ai", 
            "design-system-ai"
        ]
        
        for query in design_queries[:2]: # نأخذ استعلامين فقط لتوفير الوقت
            url = "https://api.github.com/search/repositories"
            params = {
                "q": f"{query} stars:>50 language:typescript OR language:javascript",
                "sort": "stars",
                "order": "desc",
                "per_page": "2"
            }
            r = requests.get(url, params=params, timeout=10)
            
            if r.status_code == 200:
                for repo in r.json().get("items", [])[:2]:
                    items.append({
                        "title": repo["full_name"],
                        "description": repo["description"] or "أداة تصميم واجهات مدعومة بالذكاء الاصطناعي",
                        "url": repo["html_url"],
                        "source": "AI Design Tools",
                        "stars": repo["stargazers_count"],
                        "is_free": True,
                        "quality_score": repo["stargazers_count"] + 500 # وزن إضافي لأدوات التصميم
                    })
    except Exception as e:
        logger.error(f"Design Tools Error: {str(e)}")
    return items

def scrape_trending_llms():
    """جلب معلومات عن النماذج الشهيرة مثل Kimi و MiniMax"""
    items = []
    try:
        logger.info("Checking famous LLMs repositories...")
        # البحث المباشر عن مستودعات النماذج الشهيرة
        famous_models = [
            "MoonshotAI/Kimi-k1", 
            "MiniMaxAI/MiniMax-01", 
            "Qwen/Qwen2.5", 
            "meta-llama/Llama-3"
        ]
        
        for model_repo in famous_models:
            url = f"https://api.github.com/repos/{model_repo}"
            r = requests.get(url, timeout=10)
            
            if r.status_code == 200:
                repo = r.json()
                items.append({
                    "title": repo["full_name"],
                    "description": repo["description"] or "نموذج لغوي كبير وقوي",
                    "url": repo["html_url"],
                    "source": "Famous LLMs",
                    "stars": repo["stargazers_count"],
                    "is_free": True,
                    "quality_score": 9999 # أولوية قصوى للنماذج الشهيرة
                })
    except Exception as e:
        logger.error(f"Famous LLMs Error: {str(e)}")
    return items

def scrape_all_sources():
    all_news = []
    # دمج جميع المصادر الجديدة
    all_news.extend(scrape_trending_llms())   # 1. النماذج الشهيرة أولاً
    all_news.extend(scrape_design_tools())    # 2. أدوات التصميم
    all_news.extend(scrape_github())          # 3. أدوات GitHub العامة
    all_news.extend(scrape_huggingface())     # 4. نماذج HuggingFace
    
    all_news.sort(key=lambda x: x.get("quality_score", 0), reverse=True)
    final_items = all_news[:5] 
    
    logger.info(f"Selected {len(final_items)} diverse professional tools.")
    return final_items
