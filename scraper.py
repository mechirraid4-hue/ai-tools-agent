import requests
import feedparser
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

def scrape_github_trending():
    news_items = []
    
    try:
        logger.info("Scraping GitHub Trending")
        
        url = "https://api.github.com/search/repositories"
        params = {
            'q': 'artificial intelligence license:mit',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 10
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for repo in data.get('items', [])[:5]:
            if not repo.get('description'):
                continue
            
            news_items.append({
                'title': repo['full_name'],
                'description': repo['description'],
                'url': repo['html_url'],
                'source': 'GitHub',
                'published': repo['created_at'],
                'stars': repo['stargazers_count'],
                'is_free': True
            })
        
        logger.info("Found " + str(len(news_items)) + " items from GitHub")
        
    except Exception as e:
        logger.error("Error scraping GitHub: " + str(e))
    
    return news_items

def scrape_huggingface():
    news_items = []
    
    try:
        logger.info("Scraping Hugging Face")
        
        url = "https://huggingface.co/api/models"
        params = {
            'sort': 'lastModified',
            'direction': '-1',
            'limit': 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for model in data[:5]:
            news_items.append({
                'title': model['modelId'],
                'description': "Free AI model",
                'url': "https://huggingface.co/" + model['modelId'],
                'source': 'Hugging Face',
                'published': model.get('lastModified', ''),
                'is_free': True
            })
        
        logger.info("Found " + str(len(news_items)) + " items from Hugging Face")
        
    except Exception as e:
        logger.error("Error scraping Hugging Face: " + str(e))
    
    return news_items

def scrape_rss_feeds():
    news_items = []
    
    try:
        logger.info("Scraping RSS feeds")
        
        feeds = [
            'https://openai.com/blog/rss.xml',
            'https://huggingface.co/blog/feed.xml'
        ]
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:2]:
                    news_items.append({
                        'title': entry.title,
                        'description': entry.get('summary', '')[:200],
                        'url': entry.link,
                        'source': 'RSS Feed',
                        'published': entry.get('published', ''),
                        'is_free': True
                    })
            except Exception as e:
                logger.warning("Error parsing feed: " + str(e))
        
        logger.info("Found " + str(len(news_items)) + " items from RSS")
        
    except Exception as e:
        logger.error("Error scraping RSS: " + str(e))
    
    return news_items

def scrape_all_sources():
    logger.info("Starting to scrape all sources")
    
    all_news = []
    
    all_news.extend(scrape_github_trending())
    all_news.extend(scrape_huggingface())
    all_news.extend(scrape_rss_feeds())
    
    logger.info("Total news items found: " + str(len(all_news)))
    
    return all_news            free_licenses = ['mit', 'apache-2.0', 'bsd-3-clause', 'bsd-2-clause', 'gpl-3.0', 'lgpl-3.0', 'unlicense', 'wtfpl']
            
            if license_key in free_licenses or not license_key:
                news_items.append({
                    'title': repo['full_name'],
                    'description': repo['description'],
                    'url': repo['html_url'],
                    'source': 'GitHub (' + license_name + ')',
                    'published': repo['created_at'],
                    'stars            free_licenses = ['mit', 'apache-2.0', 'bsd-3-clause', 'bsd-2-clause', 'gpl-3.0', 'lgpl-3.0', 'unlicense', 'wtfpl']
            
            # Skip if it's not a free license or has no description
            if not repo.get('description'):
                continue
                
            if license_key in free_licenses or not license_key:
                news_items.append({
                    'title': repo['full_name'],
                    'description': repo['description'],
                    'url': repo['html_url'],
                    'source': f'GitHub ({license_name})',
                    'published': repo['created_at'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'is_free': True,
                    'license': license_name
                })
        
        logger.info(f"✅ Found {len(news_items)} FREE items from GitHub")
        
    except Exception as e:
        logger.error(f"❌ Error scraping GitHub: {e}")
    
    return news_items

def scrape_huggingface():
    """Scrape latest FREE models from Hugging Face"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping Hugging Face (FREE models only)...")
        
        # Hugging Face API - filter for free models with popular licenses
        url = "https://huggingface.co/api/models"
        params = {
            'sort': 'lastModified',
            'direction': '-1',
            'limit': 15,
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for model in data[:8]:
            # Check if it's free
            pipeline_tag = model.get('pipeline_tag', '')
            tags = model.get('tags', [])
            card_data = model.get('cardData', {})
            license_info = card_data.get('license', 'Unknown')
            
            # Skip if it's a paid/gated model
            if 'gated' in tags:
                continue
            
            # Skip if no description
            if not model.get('cardData', {}).get('library_name'):
                continue
            
            news_items.append({
                'title': model['modelId'],
                'description': f"نموذج {pipeline_tag or 'AI'} مجاني - {model.get('author', 'Unknown')}",
                'url': f"https://huggingface.co/{model['modelId']}",
                'source': f'Hugging Face ({license_info})',
                'published': model.get('lastModified', ''),
                'downloads': model.get('downloads', 0),
                'likes': model.get('likes', 0),
                'is_free': True,
                'license': license_info
            })
        
        logger.info(f"✅ Found {len(news_items)} FREE items from Hugging Face")
        
    except Exception as e:
        logger.error(f"❌ Error scraping Hugging Face: {e}")
    
    return news_items

def scrape_reddit():
    """Scrape FREE AI tools news from Reddit"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping Reddit (FREE AI tools)...")
        
        # Reddit JSON API (no authentication needed)
        subreddits = ['MachineLearning', 'LocalLLaMA', 'artificial', 'opensource']
        
        for subreddit in subreddits:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {'User-Agent': 'AI Tools Agent/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for post in data['data']['children'][:3]:
                post_data = post['data']
                title = post_data['title'].lower()
                
                # Filter for free/open-source tools only
                if any(word in title for word in ['free', 'open source', 'open-source', 'opensource', 'mit', 'apache', 'gpl']):
                    news_items.append({
                        'title': post_data['title'],
                        'description': post_data.get('selftext', '')[:300] or 'مناقشة عن أداة ذكاء اصطناعي',
                        'url': f"https://reddit.com{post_data['permalink']}",
                        'source': f'Reddit r/{subreddit}',
                        'published': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                        'score': post_data['score'],
                        'is_free': True
                    })
        
        logger.info(f"✅ Found {len(news_items)} FREE items from Reddit")
        
    except Exception as e:
        logger.error(f"❌ Error scraping Reddit: {e}")
    
    return news_items

def scrape_rss_feeds():
    """Scrape FREE AI news from RSS feeds"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping RSS feeds (FREE AI announcements)...")
        
        feeds = [
            'https://openai.com/blog/rss.xml',
            'https://blog.google/technology/ai/rss/',
            'https://ai.meta.com/blog/rss/',
            'https://huggingface.co/blog/feed.xml'
        ]
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:3]:
                    title = entry.title.lower()
                    
                    # Filter for free/open announcements
                    if any(word in title for word in ['free', 'open', 'release', 'launch', 'introducing', 'announcing']):
                        news_items.append({
                            'title': entry.title,
                            'description': entry.get('summary', '')[:300] or entry.get('description', '')[:300],
                            'url': entry.link,
                            'source': feed.feed.get('title', 'Unknown'),
                            'published': entry.get('published', ''),
                            'is_free': True
                        })
            except Exception as e:
                logger.warning(f"⚠️ Error parsing {feed_url}: {e}")
        
        logger.info(f"✅ Found {len(news_items)} items from RSS feeds")
        
    except Exception as e:
        logger.error(f"❌ Error scraping RSS: {e}")
    
    return news_items

def scrape_all_sources():
    """Scrape FREE AI tools news from all sources"""
    logger.info("🌐 Starting to scrape FREE AI tools from all sources...")
    
    all_news = []
    
    # Scrape from all sources
    all_news.extend(scrape_github_trending())
    all_news.extend(scrape_huggingface())
    all_news.extend(scrape_reddit())
    all_news.extend(scrape_rss_feeds())
    
    logger.info(f"🎯 Total FREE news items found:
