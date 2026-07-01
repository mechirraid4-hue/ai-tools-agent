import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_news(news_item):
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            logger.error("GROQ_API_KEY not found!")
            raise ValueError("GROQ_API_KEY missing")
        
        client = Groq(api_key=api_key)
        
        title = news_item.get('title', '')
        desc = news_item.get('description', '')
        source = news_item.get('source', '')
        url = news_item.get('url', '')
        stars = news_item.get('stars', '')
        
        logger.info(f"Summarizing: {title}")
        
        prompt_text = (
            "أنت خبير تقني في أدوات الذكاء الاصطناعي. قدم تحليلاً شاملاً بالعربية للأداة التالية:\n\n"
            f"الاسم: {title}\n"
            f"المصدر: {source}\n"
            f"الوصف: {desc}\n"
            f"{'النجوم: ' + str(stars) if stars else ''}\n\n"
            "المطلوب بالعربية:\n"
            "1. التقييم العام (من 5 نجوم مع سبب)\n"
            "2. ما هي الأداة؟ (شرح واضح)\n"
            "3. المزايا الرئيسية (3 نقاط)\n"
            "4. خطوات الاستخدام المجاني (دليل عملي خطوة بخطوة)\n"
            "5. كيف تفيد مطور AI؟ (أمثلة عملية)\n"
            "6. العيوب والقيود\n"
            "7. الحكم النهائي (هل تنصح بها؟)\n\n"
            "كن دقيقاً وعملياً."
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أجب بالعربية الفصحى الواضحة. ركز على الجوانب العملية."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        summary = completion.choices[0].message.content
        logger.info(f"Summary generated: {len(summary)} chars")
        
        return {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary,
            'is_free': True
        }
        
    except Exception as e:
        logger.error(f"Summarizer Error: {str(e)}")
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': f"📌 **الأداة:** {news_item.get('title', '')}\n\n🔗 **الرابط:** {news_item.get('url', '')}\n\n💡 **ملاحظة:** تحقق من الوثائق الرسمية للتفاصيل.",
            'is_free': True
        }
