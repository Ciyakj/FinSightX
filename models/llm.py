import requests
import streamlit as st

def call_llm(prompt, model="groq", mode="concise"):
    try:
        if model == "groq":
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "llama2-70b-4096",  # safer fallback model
                "messages": [
                    {"role": "system", "content": f"You are a financial analysis assistant. Give {mode} answers."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
        else:
            return "Model not configured."
    except Exception as e:
        return f"LLM Error: {str(e)}"
