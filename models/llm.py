
from config.config import GROQ_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY
import requests

def call_llm(prompt, model="groq", mode="concise"):
    try:
        if model == "groq":
            url = "https://api.groq.com/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            body = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": f"You are a financial analysis assistant. Give {mode} answers."},
                    {"role": "user", "content": prompt}
                ]
            }
            r = requests.post(url, headers=headers, json=body)
            return r.json()["choices"][0]["message"]["content"]
        return "Model not configured"
    except Exception as e:
        return f"LLM Error: {str(e)}"
