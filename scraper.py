import requests
import feedparser
import logging
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

def scrape_github_trending():
    """Scrape trending AI repositories from GitHub"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping GitHub Trending...")
        
        # GitHub Trending API (unofficial)
        url = "https://api.github.com/search/repositories"
        params = {
            'q': 'artificial intelligence OR machine learning OR deep learning',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 5
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for repo in data.get('items', [])[:5]:
            news_items.append({
                'title': repo['full_name'],
                'description': repo['description'] or 'No description',
                'url': repo['html_url'],
                'source': 'GitHub Trending',
                'published': repo['created_at'],
                'stars': repo['stargazers_count']
            })
        
        logger.info(f"✅ Found {len(news_items)} items from GitHub")
        
    except Exception as e:
        logger.error(f"❌ Error scraping GitHub: {e}")
    
    return news_items

def scrape_huggingface():
    """Scrape latest models from Hugging Face"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping Hugging Face...")
        
        # Hugging Face API
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
                'description': f"Model by {model.get('author', 'Unknown')}",
                'url': f"https://huggingface.co/{model['modelId']}",
                'source': 'Hugging Face',
                'published': model.get('lastModified', ''),
                'downloads': model.get('downloads', 0)
            })
        
        logger.info(f"✅ Found {len(news_items)} items from Hugging Face")
        
    except Exception as e:
        logger.error(f"❌ Error scraping Hugging Face: {e}")
    
    return news_items

def scrape_reddit():
    """Scrape AI news from Reddit"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping Reddit...")
        
        # Reddit JSON API (no authentication needed)
        subreddits = ['MachineLearning', 'LocalLLaMA', 'artificial']
        
        for subreddit in subreddits:
            url = f"https://www.reddit.com/r/{subreddit}/hot.json"
            headers = {'User-Agent': 'AI Tools Agent/1.0'}
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            for post in data['data']['children'][:2]:
                post_data = post['data']
                news_items.append({
                    'title': post_data['title'],
                    'description': post_data.get('selftext', '')[:200],
                    'url': f"https://reddit.com{post_data['permalink']}",
                    'source': f'Reddit r/{subreddit}',
                    'published': datetime.fromtimestamp(post_data['created_utc']).isoformat(),
                    'score': post_data['score']
                })
        
        logger.info(f"✅ Found {len(news_items)} items from Reddit")
        
    except Exception as e:
        logger.error(f"❌ Error scraping Reddit: {e}")
    
    return news_items

def scrape_rss_feeds():
    """Scrape AI news from RSS feeds"""
    news_items = []
    
    try:
        logger.info("🔍 Scraping RSS feeds...")
        
        feeds = [
            'https://openai.com/blog/rss.xml',
            'https://blog.google/technology/ai/rss/',
            'https://ai.meta.com/blog/rss/'
        ]
        
        for feed_url in feeds:
            try:
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:2]:
                    news_items.append({
                        'title': entry.title,
                        'description': entry.get('summary', '')[:200],
                        'url': entry.link,
                        'source': feed.feed.get('title', 'Unknown'),
                        'published': entry.get('published', '')
                    })
            except Exception as e:
                logger.warning(f"⚠️ Error parsing {feed_url}: {e}")
        
        logger.info(f"✅ Found {len(news_items)} items from RSS feeds")
        
    except Exception as e:
        logger.error(f"❌ Error scraping RSS: {e}")
    
    return news_items

def scrape_all_sources():
    """Scrape news from all sources"""
    logger.info("🌐 Starting to scrape all sources...")
    
    all_news = []
    
    # Scrape from all sources
    all_news.extend(scrape_github_trending())
    all_news.extend(scrape_huggingface())
    all_news.extend(scrape_reddit())
    all_news.extend(scrape_rss_feeds())
    
    logger.info(f"🎯 Total news items found: {len(all_news)}")
    
    return all_news
