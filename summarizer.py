import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_news(news_item):
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found")
        
        client = Groq(api_key=api_key)
        
        title = news_item.get('title', '')
        description = news_item.get('description', '')
        source = news_item.get('source', '')
        url = news_item.get('url', '')
        
        prompt = """أنت خبير في أدوات الذكاء الاصطناعي المجانية. قدّم وصفاً شاملاً بالعربية:

العنوان: """ + title + """
الوصف: """ + description + """

المطلوب:
1. عنوان جذاب
2. ما هي هذه الأداة؟ (2-3 جمل)
3. المزايا الرئيسية (3 نقاط)
4. لماذا مهمة؟

كن دقيقاً وواقعياً."""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت مساعد خبير في الذكاء الاصطناعي. أجب بالعربية."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        summary_text = completion.choices[0].message.content
        
        return {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary_text,
            'original_description': description,
            'is_free': True
        }
        
    except Exception as e:
        logger.error("Error summarizing: " + str(e))
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': news_item.get('description', ''),
            'original_description': news_item.get('description', ''),
            'is_free': True
        }              {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        
        summary_text = completion.choices[0].message.content
        
        return {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary_text,
            'original_description': description,
            'is_free': True
        }
        
    except Exception as e:
        logger.error("Error summarizing: " + str(e))
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': news_item.get('description', ''),
            'original_description': news_item.get('description', ''),
            'is_free': True
        }
