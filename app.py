import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.file_reader import read_financial_files
from utils.rag_retriever import FinancialRAG

st.set_page_config(page_title="FinSightX")
st.title("📊 FinSightX – Analyze Company Financials Intelligently")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "document_chunks" not in st.session_state:
    st.session_state.document_chunks = []

# UI Controls
mode = st.selectbox("Choose response mode", ["concise", "detailed"])
model = st.selectbox("Choose LLM model", ["groq", "gemini", "deepseek"])
company_name = st.text_input("Enter Company Name (e.g., Infosys)")
uploaded_files = st.file_uploader("Upload Financial Documents (PDF, CSV)", type=["pdf", "csv"], accept_multiple_files=True)

# Ingest uploaded documents
if uploaded_files:
    st.info("📂 Reading uploaded financial documents...")
    chunks = read_financial_files(uploaded_files)
    if chunks:
        st.session_state.document_chunks.extend(chunks)
        st.success(f"✅ Loaded {len(chunks)} text chunks from uploaded files.")
    else:
        st.warning("⚠️ No readable text found in uploaded documents.")

# Scrape if company name is given
if company_name and not uploaded_files:
    st.info("🔍 Scraping data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(company_name)
    if isinstance(dfs, list):
        chunks = [df.to_string(index=False) for df in dfs if isinstance(df, pd.DataFrame)]
        if chunks:
            st.session_state.document_chunks.extend(chunks)
            st.success(f"✅ Retrieved and chunked financial data from Moneycontrol for {company_name}.")
        else:
            st.warning("⚠️ No usable data found in scraped tables.")
    else:
        st.warning(f"❌ Error: {dfs}")

# Chat Input
user_input = st.chat_input("Chat with FinSightX")
if user_input:
    st.session_state.chat_history.append(("user", user_input))

    # RAG retrieval
    context = ""
    if st.session_state.document_chunks:
        try:
            rag = FinancialRAG()
            rag.add_chunks(st.session_state.document_chunks)
            top_chunks = rag.query(user_input)
            context = "\n\n".join(top_chunks)
        except Exception as e:
            st.warning(f"⚠️ RAG Error: {e}")
            context = ""

    full_prompt = f"Context:\n{context}\n\nUser question: {user_input}\nAnswer in {mode} mode."
    llm_response = call_llm(full_prompt, model=model)
    st.session_state.chat_history.append(("bot", llm_response))

# Chat display
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)

# Fallback info
if not uploaded_files and not company_name:
    st.info("📥 Upload a financial file or enter a company name to begin.")
