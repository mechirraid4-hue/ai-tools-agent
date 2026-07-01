import os
import logging
from groq import Groq

logger = logging.getLogger(__name__)

def summarize_news(news_item):
    try:
        api_key = os.environ.get('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY missing")
        
        client = Groq(api_key=api_key)
        
        title = news_item.get('title', '')
        desc = news_item.get('description', '')
        source = news_item.get('source', '')
        url = news_item.get('url', '')
        item_type = news_item.get('type', 'tool')  # تحديد نوع المحتوى
        
        # برومبت ديناميكي يتغير حسب نوع المحتوى
        if item_type == "update":
            prompt_text = (
                "أنت خبير تقني متخصص في أطر عمل الذكاء الاصطناعي. لقد صدر تحديث جديد للأداة التالية:\n\n"
                f"الأداة: {title}\n"
                f"المصدر: {source}\n"
                f"تفاصيل التحديث: {desc}\n\n"
                "مهمتك: تقديم شرح عملي بالعربية يركز على الفائدة للمطور:\n"
                "1. ما الجديد؟ (شرح بسيط للتغيير التقني)\n"
                "2. لماذا هذا مهم؟ (هل يحسن الأداء؟ يصلح ثغرة؟ يضيف دعماً للغة العربية؟)\n"
                "3. كيف تستخدمه؟ (مثال كود Python قصير أو أمر تثبيت محدد)\n"
                "4. هل يتطلب ترقية فورية أم يمكن تأجيله؟\n\n"
                "كن دقيقاً وعملياً. تجنب الكلام الإنشائي."
            )
        else:
            prompt_text = (
                "أنت خبير تقني محايد. حلل أداة الذكاء الاصطناعي المجانية التالية وقدم تقريراً بالعربية:\n\n"
                f"الأداة: {title}\n"
                f"المصدر: {source}\n"
                f"الوصف: {desc}\n\n"
                "التقرير المطلوب:\n"
                "1. تقييم عام (من 5 نجوم مع تبرير)\n"
                "2. ما هي الأداة؟ (شرح واضح لوظيفتها)\n"
                "3. المزايا الرئيسية (3 نقاط عملية)\n"
                "4. خطوات الاستخدام المجاني (دليل سريع)\n"
                "5. كيف تفيد مطور AI في بناء تطبيقاته؟\n"
                "6. الحكم النهائي (هل تنصح بها؟)\n\n"
                "كن واقعياً ودقيقاً."
            )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أجب دائماً بالعربية الفصحى الواضحة والمباشرة. ركز على الجوانب التقنية والعملية."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        return {
            'title': title,
            'url': url,
            'source': source,
            'summary': completion.choices[0].message.content,
            'is_free': True
        }
        
    except Exception as e:
        logger.error(f"Summarizer Fallback Triggered: {str(e)}")
        # خطة بديلة عند فشل الاتصال بالذكاء الاصطناعي
        fallback = (
            f"📌 **ملخص:** {news_item.get('description', 'أداة/تحديث تقني جديد.')}\n\n"
            f"🔗 **الرابط الرسمي:** {news_item.get('url', '')}\n\n"
            f"💡 **نصيحة:** تحقق من الوثائق الرسمية للحصول على تفاصيل التثبيت والاستخدام."
        )
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': fallback,
            'is_free': True
        }
