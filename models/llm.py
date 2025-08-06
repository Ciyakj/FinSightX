import requests
import streamlit as st

def call_llm(prompt, model="groq", mode="concise"):
    try:
        if model == "groq":
            url = "https://api.groq.com/v1/chat/completions"  # ✅ correct endpoint
            headers = {
                "Authorization": f"Bearer {st.secrets['GROQ_API_KEY']}",
                "Content-Type": "application/json"
            }
            body = {
                "model": "mixtral-8x7b-32768",  # or any other supported model
                "messages": [
                    {"role": "system", "content": f"You are a financial assistant. Answer in a {mode} manner."},
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
