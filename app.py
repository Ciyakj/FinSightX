import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.file_reader import read_financial_files
from utils.rag_retriever import FinancialRAG

st.set_page_config(page_title="FinSightX", layout="wide")
st.title("📊 FinSightX – Analyze Company Financials Intelligently")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

mode = st.selectbox("Choose response mode", ["concise", "detailed"])
model = st.selectbox("Choose LLM model", ["groq", "gemini", "deepseek"])
company_name = st.text_input("Enter Company Name (e.g., Infosys)")
uploaded_files = st.file_uploader("Upload Financial Documents (PDF, CSV)", type=["pdf", "csv"], accept_multiple_files=True)
question = st.text_input("Ask something about the financials:")

# Display chat history
if st.session_state.chat_history:
    st.markdown("### 🧠 Chat History")
    for i, (q, a) in enumerate(st.session_state.chat_history):
        st.markdown(f"**🧑 You:** {q}")
        st.markdown(f"**🤖 Bot:** {a}")
        st.markdown("---")

# Handler for new question
if question:
    try:
        # Collect context from uploaded files
        context_chunks = []

        if uploaded_files:
            st.info("📂 Reading uploaded financial documents...")
            context_chunks.extend(read_financial_files(uploaded_files))

        elif company_name:
            st.info("🌐 Scraping financial data from Moneycontrol...")
            dfs = fetch_moneycontrol_financials(company_name)
            if isinstance(dfs, list):
                for df in dfs:
                    if isinstance(df, pd.DataFrame):
                        context_chunks.append(df.to_string(index=False))
            else:
                st.warning(f"❌ Scraping error: {dfs}")

        # Retrieve relevant context using RAG
        rag = FinancialRAG()
        rag.add_chunks(context_chunks)
        retrieved_context = "\n\n".join(rag.query(question))

        # Build full prompt with recent memory
        conversation_context = ""
        for prev_q, prev_a in st.session_state.chat_history[-3:]:  # Use last 3 messages
            conversation_context += f"User: {prev_q}\nAI: {prev_a}\n"

        full_prompt = f"{conversation_context}\nContext:\n{retrieved_context}\n\nUser: {question}"
        response = call_llm(full_prompt)

        # Save to chat history
        st.session_state.chat_history.append((question, response))

        # Refresh page to show chat history
        st.rerun()

    except Exception as e:
        st.error(f"Something went wrong: {e}")

else:
    st.info("📥 Upload a financial file or enter a company name to begin.")
