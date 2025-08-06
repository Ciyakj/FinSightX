from config.config import GROQ_API_KEY, GEMINI_API_KEY, DEEPSEEK_API_KEY
import requests

def call_llm(prompt, model="groq", mode="concise"):
    try:
        if model == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "mixtral-8x7b-32768",
                "messages": [
                    {"role": "system", "content": f"You are a financial analysis assistant. Give {mode} answers."},
                    {"role": "user", "content": prompt}
                ]
            }
            r = requests.post(url, headers=headers, json=body)
            r.raise_for_status()
            result = r.json()

            # ✅ Safely check for choices
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"].strip()
            else:
                return "LLM Error: No response choices returned from Groq."

        return "Model not configured"
    except Exception as e:
        return f"LLM Error: {str(e)}"
