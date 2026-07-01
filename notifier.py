import os
import logging
import requests

logger = logging.getLogger(__name__)

def send_to_telegram(summary):
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            raise ValueError("Telegram creds missing")
        
        title = summary.get('title', 'أداة جديدة')
        url = summary.get('url', '')
        source = summary.get('source', '')
        text = summary.get('summary', '')
        
        # تنسيق الرسالة مع إيموجي واضح
        message = f"""🤖 <b>أداة ذكاء اصطناعي قوية</b>

📌 <b>{title}</b>

{text}

 <a href="{url}">رابط الأداة الرسمي</a>
📍 المصدر: {source}

━━━━━━━━━━━━━━━━━━━━
✅ مجانية 100% - مختارة بعناية"""

        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }
        
        r = requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", json=payload, timeout=10)
        r.raise_for_status()
        logger.info(f"Sent: {title[:30]}")
        return True
        
    except Exception as e:
        logger.error(f"Telegram Error: {str(e)}")
        return False        
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML',
            'disable_web_page_preview': False
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        response.raise_for_status()
        
        logger.info(f"✅ Sent to Telegram: {title[:50]}...")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending to Telegram: {e}")
        return False

def send_startup_message():
    """Send a startup message to Telegram"""
    
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            return False
        
        message = "🚀 <b>AI Tools Agent</b>\n\nبدأت عملية البحث عن أحدث أدوات الذكاء الاصطناعي..."
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        response.raise_for_status()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending startup message: {e}")
        return False

def send_completion_message(total_sent):
    """Send a completion message to Telegram"""
    
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            return False
        
        message = f"""✅ <b>اكتمل البحث!</b>

📊 تم إرسال {total_sent} أداة جديدة

🔄 سأعود بعد ساعة للبحث عن المزيد..."""
        
        telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(telegram_url, json=payload, timeout=10)
        response.raise_for_status()
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error sending completion message: {e}")
        return False
