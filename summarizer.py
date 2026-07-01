import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_news(news_item):
    """Summarize news item using Groq AI in Arabic"""
    
    try:
        # Initialize Groq client
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        client = Groq(api_key=api_key)
        
        # Prepare the prompt
        title = news_item.get('title', '')
        description = news_item.get('description', '')
        source = news_item.get('source', '')
        url = news_item.get('url', '')
        
        prompt = f"""أنت خبير في تحليل أخبار الذكاء الاصطناعي. قم بتلخيص الخبر التالي بالعربية بشكل احترافي ومختصر.

المصدر: {source}
العنوان: {title}
الوصف: {description}

المطلوب:
1. عنوان جذاب بالعربية (سطر واحد)
2. ملخص مختصر (2-3 جمل)
3. لماذا هذا الخبر مهم؟ (جملة واحدة)

أجب بتنسيق واضح ومنظم."""

        # Call Groq API
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت مساعد خبير في الذكاء الاصطناعي. أجب دائمًا بالعربية."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500,
            top_p=1,
            stream=False
        )
        
        # Extract the summary
        summary_text = completion.choices[0].message.content
        
        # Format the output
        result = {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary_text,
            'original_description': description
        }
        
        logger.info(f"✅ Summarized: {title[:50]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ Error summarizing news: {e}")
        
        # Return original news if summarization fails
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': news_item.get('description', ''),
            'original_description': news_item.get('description', '')
        }
