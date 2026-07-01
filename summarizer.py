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
        stars = news_item.get('stars', '')
        downloads = news_item.get('downloads', '')
        license_info = news_item.get('license', '')
        
        prompt = """أنت خبير تقني متخصص في تقييم أدوات الذكاء الاصطناعي المفتوحة المصدر والمجانية.

مهمتك: تحليل دقيق وشامل للأداة التالية وتقديم تقرير احترافي بالعربية.

معلومات الأداة:
- العنوان: """ + title + """
- المصدر: """ + source + """
- الوصف: """ + description + """
""" + (" - النجوم: " + str(stars) if stars else "") + """
""" + (" - التنزيلات: " + str(downloads) if downloads else "") + """
""" + (" - الترخيص: " + str(license_info) if license_info else "") + """

قدّم التقرير التالي بدقة وواقعية:

⭐ **التقييم العام:** (من 5 نجوم مع تبرير مختصر)

🏢 **الجهة المطورة:**
(من طوّر هذه الأداة؟ شركة كبرى؟ منظمة بحثية؟ مطور مستقل؟ مجتمع مفتوح المصدر؟ ما مصداقيتها؟)

🎯 **الجمهور المستهدف:**
(لمن هذه الأداة؟ مطورون محترفون؟ باحثون؟ مبتدئون؟ شركات؟)

📌 **ما هي الأداة؟**
(2-3 جمل دقيقة تشرح الوظيفة الأساسية والتقنيات المستخدمة)

✨ **المزايا الرئيسية:**
(3-4 مزايا محددة وعملية)

⚠️ **العيوب والقيود:**
(اذكر بصدق أي قيود أو مشاكل معروفة)

📚 **دليل الاستخدام المجاني خطوة بخطوة:**
1. التثبيت/الوصول (أمر محدد)
2. المتطلبات التقنية
3. خطوات عملية للاستخدام
4. مثال كود بسيط إن أمكن

💡 **كيف تفيدني كمطور AI؟**
(3-4 حالات استخدام محددة ومباشرة لمطور يريد بناء تطبيقات ذكاء اصطناعي)

📊 **مقارنة سريعة:**
(كيف تقارن بالبدائل الشهيرة؟ ما ميزتها التنافسية؟)

✅ **التوصية النهائية:**
(هل أنصح باستخدامها؟ في أي حالة؟)

كن دقيقاً، واقعياً، وصادقاً. لا تبالغ في المديح. ركّز على القيمة العملية."""

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "أنت خبير تقني محايد ودقيق. قدّم تقييمات واقعية وصادقة للأدوات. لا تبالغ في الإيجابيات ولا تتجاهل السلبيات. أجب بالعربية الفصحى الواضحة."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1200,
            top_p=0.9
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
