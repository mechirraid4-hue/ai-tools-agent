import os
import logging
import requests

logger = logging.getLogger(__name__)

def send_to_telegram(summary):
    try:
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            logger.error("Telegram credentials missing!")
            return False
        
        title = summary.get('title', 'AI Tool')
        url = summary.get('url', '')
        source = summary.get('source', '')
        text = summary.get('summary', '')
        
        message = f"""🤖 <b>أداة ذكاء اصطناعي قوية</b>

📌 <b>{title}</b>

{text}

🔗 <a href="{url}">رابط الأداة الرسمي</a>
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
        logger.info(f"Sent to Telegram: {title[:30]}")
        return True
        
    except Exception as e:
        logger.error(f"Telegram Error: {str(e)}")
        return False
