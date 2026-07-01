 import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_news(news_item):
    """Summarize FREE AI tool with detailed Arabic description focusing on features"""
    
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
        stars = news_item.get('stars', '')
        forks = news_item.get('forks', '')
        downloads = news_item.get('downloads', '')
        likes = news_item.get('likes', '')
        license_info = news_item.get('license', 'مفتوح المصدر')
        
        prompt = f"""أنت خبير تقني متخصص في أدوات الذكاء الاصطناعي المجانية والمفتوحة المصدر. قدّم تحليلاً دقيقاً وشاملاً بالعربية للأداة التالية:

🔹 **المعلومات الأساسية:**
- المصدر: {source}
- العنوان: {title}
- الترخيص: {license_info}
- الوصف الأصلي: {description}
{"- ⭐ عدد النجوم: " + str(stars) if stars else ""}
{"- 🔀 عدد forks: " + str(forks) if forks else ""}
{"- 📥 عدد التنزيلات: " + str(downloads) if downloads else ""}
{"- ❤️ عدد الإعجابات: " + str(likes) if likes else ""}

🎯 **المطلوب (بالعربية الفصحى الواضحة):**

**1. العنوان الرئيسي:** (عنوان جذاب ومختصر يعكس جوهر الأداة)

**2. ما هي هذه الأداة؟**
(2-3 جمل تشرح بوضوح: ما هي؟ ماذا تفعل؟ لمن موجهة؟)

**3. المزايا والخصائص الرئيسية:**
(اذكر 3-5 مزايا محددة وواضحة، ركّز على:
- ما الذي يميزها عن غيرها؟
- ما التقنيات المستخدمة؟
- ما المشكلات التي تحلها؟
- هل سهلة الاستخدام؟)

**4. حالات الاستخدام:**
(أمثلة عملية: متى ولماذا تستخدم هذه الأداة؟)

**5. لماذا مهمة؟**
(جملة واحدة توضح القيمة المضافة والأهمية)

**6. متطلبات الاستخدام:**
(سطر واحد: هل تحتاج خبرة؟ هل تتطلب دفع؟ إلخ)

⚠️ **ملاحظات مهمة:**
- كن دقيقاً وواقعياً
- تجنب المبالغة
- ركّز على الجوانب العملية
- استخدم لغة عربية فصحى واضحة
- تأكد من أن الوصف مناسب للمبتدئين والمحترفين"""

        # Call Groq API with enhanced settings
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت خبير تقني في الذكاء الاصطناعي والأدوات المفتوحة المصدر. قدّم أوصافاً دقيقة وشاملة بالعربية الفصحى، مع التركيز على المزايا العملية والاستخدامات الواقعية. كن واضحاً وموجزاً."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.6,
            max_tokens=800,
            top_p=0.9,
            stream=False,
            stop=None
        )
        
        # Extract the summary
        summary_text = completion.choices[0].message.content
        
        # Clean and format the summary
        summary_text = summary_text.strip()
        
        # Format the output
        result = {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary_text,
            'original_description': description,
            'is_free': True,
            'license': license_info
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
            'summary': f" {news_item.get('description', '')}\n\n⚠️ لم يتم توليد وصف تفصيلي",
            'original_description': news_item.get('description', ''),
            'is_free': True,
            'license': news_item.get('license', 'مفتوح المصدر')
        }       # Call Groq API
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
