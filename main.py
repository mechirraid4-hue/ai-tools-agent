import os
import logging
import json
from datetime import datetime
from scraper import scrape_all_sources
from summarizer import summarize_news
from notifier import send_to_telegram

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_sent_news():
    try:
        with open('sent_news.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def save_sent_news(sent_data):
    with open('sent_news.json', 'w') as f:
        json.dump(sent_data, f, indent=2)

def main():
    logger.info("🚀 Starting AI Tools Agent...")
    
    news_items = scrape_all_sources()
    logger.info(f"📰 Found {len(news_items)} tools")
    
    if not news_items:
        logger.warning("⚠️ No tools found. Exiting.")
        return
    
    sent_news = load_sent_news()
    
    sent_count = 0
    for item in news_items:
        url = item.get('url', '')
        
        if url in sent_news:
            logger.info(f"⏭️ Already sent: {item.get('title', '')}")
            continue
        
        logger.info(f"🔄 Processing: {item.get('title', '')}")
        
        summary_data = summarize_news(item)
        
        success = send_to_telegram(summary_data)
        
        if success:
            sent_news[url] = {
                'title': item.get('title', ''),
                'sent_at': datetime.now().isoformat(),
                'source': item.get('source', '')
            }
            sent_count += 1
            logger.info(f"✅ Sent: {item.get('title', '')}")
        else:
            logger.error(f"❌ Failed to send: {item.get('title', '')}")
    
    save_sent_news(sent_news)
    
    logger.info(f"🎉 Total sent: {sent_count}")

if __name__ == "__main__":
    main()
