import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.file_reader import read_financial_files
from utils.rag_retriever import FinancialRAG

st.set_page_config(page_title="FinSightX")
st.title("📊 FinSightX – Analyze Company Financials Intelligently")

# --- Session state ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = []

# --- Sidebar settings ---
with st.sidebar:
    st.header("⚙️ Settings")
    mode = st.selectbox("Choose response mode", ["concise", "detailed"])
    model = st.selectbox("Choose LLM model", ["groq", "gemini", "deepseek"])
    company_name = st.text_input("Enter Company Name (e.g., Infosys)")
    uploaded_files = st.file_uploader("Upload Financial Documents (PDF, CSV)", type=["pdf", "csv"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            chunks = read_financial_files(file)
            st.session_state.document_chunks.extend(chunks)

    elif company_name:
        st.info("🔍 Scraping data from Moneycontrol...")
        dfs = fetch_moneycontrol_financials(company_name)
        if isinstance(dfs, list):
            for df in dfs:
                if isinstance(df, pd.DataFrame):
                    st.session_state.document_chunks.append(df.to_string(index=False))
        else:
            st.warning(f"❌ Error: {dfs}")

# --- Chat interface ---
st.subheader("💬 Chat with FinSightX")

for msg in st.session_state.chat_history:
    with st.chat_message("user"):
        st.markdown(msg["user"])
    with st.chat_message("ai"):
        st.markdown(msg["bot"])

# --- Input box at bottom ---
user_input = st.chat_input("Ask something about the financials...")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    rag = FinancialRAG()
    rag.add_chunks(st.session_state.document_chunks)
    context = "\n\n".join(rag.query(user_input))

    prompt = f"Here is the relevant financial context:\n{context}\n\nUser question: {user_input}"
    answer = call_llm(prompt)

    with st.chat_message("ai"):
        st.markdown(answer)

    # Save conversation
    st.session_state.chat_history.append({"user": user_input, "bot": answer})
