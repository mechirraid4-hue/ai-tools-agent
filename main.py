import os
import sys
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the AI tools discovery agent"""
    logger.info("=" * 60)
    logger.info("🚀 Starting AI Tools Discovery Agent")
    logger.info(f"📅 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 60)
    
    try:
        # Import modules
        from scraper import scrape_all_sources
        from summarizer import summarize_news
        from notifier import send_to_telegram
        from database import Database
        
        # Initialize database
        db = Database()
        logger.info("✅ Database initialized")
        
        # Step 1: Scrape news from all sources
        logger.info("\n📡 Step 1: Scraping news from sources...")
        raw_news = scrape_all_sources()
        logger.info(f"✅ Found {len(raw_news)} news items")
        
        if not raw_news:
            logger.info("⚠️ No new news found. Exiting.")
            return
        
        # Step 2: Filter out already sent news
        logger.info("\n🔍 Step 2: Filtering already sent news...")
        new_news = []
        for news in raw_news:
            if not db.is_sent(news['url']):
                new_news.append(news)
        
        logger.info(f"✅ {len(new_news)} new items to process")
        
        if not new_news:
            logger.info("⚠️ All news already sent. Exiting.")
            return
        
        # Step 3: Summarize news using AI
        logger.info("\n🤖 Step 3: Summarizing news with AI...")
        summarized_news = []
        for news in new_news:
            try:
                summary = summarize_news(news)
                summarized_news.append(summary)
                logger.info(f"✅ Summarized: {news['title'][:50]}...")
            except Exception as e:
                logger.error(f"❌ Error summarizing {news['title']}: {e}")
        
        logger.info(f"✅ Summarized {len(summarized_news)} items")
        
        if not summarized_news:
            logger.info("⚠️ No summaries generated. Exiting.")
            return
        
        # Step 4: Send to Telegram
        logger.info("\n📤 Step 4: Sending to Telegram...")
        for summary in summarized_news:
            try:
                send_to_telegram(summary)
                db.mark_as_sent(summary['url'])
                logger.info(f"✅ Sent: {summary['title'][:50]}...")
            except Exception as e:
                logger.error(f"❌ Error sending {summary['title']}: {e}")
        
        logger.info("\n" + "=" * 60)
        logger.info("🎉 Agent completed successfully!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
