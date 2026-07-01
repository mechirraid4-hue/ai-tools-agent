import os
import logging
import json
from datetime import datetime
from scraper import scrape_all_sources
from summarizer import summarize_news
from notifier import send_to_telegram

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    logger.info("🚀 STARTING AGENT...")
    
    # تحقق من المتغيرات
    if not os.environ.get('GROQ_API_KEY'):
        logger.error("❌ GROQ_API_KEY MISSING!")
    else:
        logger.info("✅ GROQ_API_KEY found")
        
    if not os.environ.get('TELEGRAM_BOT_TOKEN'):
        logger.error("❌ TELEGRAM_BOT_TOKEN MISSING!")
    
    # جلب الأدوات
    items = scrape_all_sources()
    logger.info(f"📰 Found {len(items)} items")
    
    if not items:
        logger.error("❌ NO ITEMS FOUND!")
        return
    
    sent = {}
    try:
        with open('sent_news.json', 'r') as f:
            sent = json.load(f)
    except:
        pass
    
    count = 0
    for item in items:
        url = item.get('url', '')
        if url in sent:
            logger.info(f"⏭️ Already sent: {item.get('title')}")
            continue
            
        logger.info(f"🔄 SUMMARIZING: {item.get('title')}")
        summary = summarize_news(item)
        
        logger.info(f"📤 SENDING TO TELEGRAM...")
        if send_to_telegram(summary):
            sent[url] = {'sent_at': datetime.now().isoformat()}
            count += 1
            logger.info(f"✅ SENT!")
        else:
            logger.error("❌ SEND FAILED!")
    
    with open('sent_news.json', 'w') as f:
        json.dump(sent, f)
    
    logger.info(f"🎉 DONE: {count} sent")

if __name__ == "__main__":
    main()
