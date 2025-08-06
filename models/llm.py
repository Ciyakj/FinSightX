from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

def call_llm(prompt, mode="concise"):
    try:
        chat = ChatGroq(
            api_key=st.secrets["GROQ_API_KEY"],
            model="mixtral-8x7b-32768"
        )

        messages = [
            SystemMessage(content=f"You are a financial assistant. Be {mode}."),
            HumanMessage(content=prompt)
        ]

        response = chat.invoke(messages)
        return response.content

    except Exception as e:
        return f"LLM Error: {str(e)}"
