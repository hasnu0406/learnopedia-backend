import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from environment variables!")

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

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

Be warm, specific, and encouraging. Use clear headings and bullet points.
"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500
        }
        response = requests.post(GROQ_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"AI error: {str(e)}")