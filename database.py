import os
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Database:
    """Simple database using JSON file to track sent news"""
    
    def __init__(self, db_file='sent_news.json'):
        """Initialize database"""
        self.db_file = db_file
        self.data = self._load_data()
        logger.info(f"✅ Database loaded: {len(self.data.get('sent_urls', []))} URLs tracked")
    
    def _load_data(self):
        """Load data from JSON file"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return {
                    'sent_urls': [],
                    'last_run': None,
                    'total_sent': 0
                }
        except Exception as e:
            logger.error(f"❌ Error loading database: {e}")
            return {
                'sent_urls': [],
                'last_run': None,
                'total_sent': 0
            }
    
    def _save_data(self):
        """Save data to JSON file"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
            logger.info("✅ Database saved")
        except Exception as e:
            logger.error(f"❌ Error saving database: {e}")
    
    def is_sent(self, url):
        """Check if URL was already sent"""
        return url in self.data.get('sent_urls', [])
    
    def mark_as_sent(self, url):
        """Mark URL as sent"""
        if url not in self.data['sent_urls']:
            self.data['sent_urls'].append(url)
            self.data['total_sent'] = self.data.get('total_sent', 0) + 1
            self.data['last_run'] = datetime.now().isoformat()
            self._save_data()
            logger.info(f"✅ Marked as sent: {url}")
    
    def get_stats(self):
        """Get database statistics"""
        return {
            'total_urls': len(self.data.get('sent_urls', [])),
            'total_sent': self.data.get('total_sent', 0),
            'last_run': self.data.get('last_run')
        }
