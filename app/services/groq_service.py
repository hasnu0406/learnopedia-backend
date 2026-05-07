import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY missing from .env file!")

client = Groq(api_key=GROQ_API_KEY)

def get_recommendations(interests: list, skills: list, goals: list) -> str:
    prompt = f"""
You are Learnopedia AI, an expert educational advisor. Based on the user profile below, provide a detailed, personalized course recommendation and learning path.

User Profile:
- Interests: {', '.join(interests)}
- Current Skills: {', '.join(skills)}
- Goals: {', '.join(goals)}

Please provide:
1. Top 5 recommended courses (with platform, duration, and why it fits them)
2. A structured 6-month learning path with monthly milestones
3. Key skills they will gain
4. Career outcomes they can expect

Be warm, specific, and encouraging.
"""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error code: {str(e)}")