import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("OPENROUTER_API_KEY is missing from environment variables!")

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

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
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/llama-3-70b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 1500
        }
        response = requests.post(OPENROUTER_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        raise Exception(f"AI error: {str(e)}")