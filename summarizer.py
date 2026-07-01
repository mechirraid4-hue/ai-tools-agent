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
        stars = news_item.get('stars', '')
        downloads = news_item.get('downloads', '')
        
        # بناء البرومبت بدقة وبدون إيموجي لتجنب أخطاء البناء
        prompt_text = (
            "You are a strict technical expert in AI tools. Analyze this tool and provide a comprehensive report in Arabic:\n\n"
            "Tool Info:\n"
            "- Name: " + title + "\n"
            "- Source: " + source + "\n"
            "- Description: " + desc + "\n"
            + ("- Stars: " + str(stars) if stars else "") + "\n"
            + ("- Downloads: " + str(downloads) if downloads else "") + "\n\n"
            "Required Report (in Arabic):\n"
            "1. Overall Rating (out of 5 stars with brief justification)\n"
            "2. Developer & Credibility (Who made it? Is it trustworthy?)\n"
            "3. Target Audience (Who is this for?)\n"
            "4. What is this tool? (2-3 clear sentences)\n"
            "5. Key Features (3-4 practical advantages)\n"
            "6. Limitations & Weaknesses (Be honest about constraints)\n"
            "7. Step-by-Step Free Usage Guide (How to start using it now)\n"
            "8. How does it help an AI developer? (Specific use cases for building apps)\n"
            "9. Quick Comparison (How does it compare to famous alternatives?)\n"
            "10. Final Verdict (Do you recommend it? Why?)\n\n"
            "Note: Be precise, realistic, and practical. Focus on technical value."
        )

        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a neutral technical analyst. Provide accurate, realistic evaluations in clear Arabic."},
                {"role": "user", "content": prompt_text}
            ],
            temperature=0.5,
            max_tokens=1200
        )
        
        summary_text = completion.choices[0].message.content
        
        return {
            'title': title,
            'url': url,
            'source': source,
            'summary': summary_text,
            'is_free': True
        }
        
    except Exception as e:
        logger.error(f"Summarizer Error: {str(e)}")
        # في حالة الخطأ، نعيد الوصف الأصلي حتى لا تظهر الرسالة فارغة
        return {
            'title': news_item.get('title', ''),
            'url': news_item.get('url', ''),
            'source': news_item.get('source', ''),
            'summary': news_item.get('description', ''),
            'is_free': True
        }
