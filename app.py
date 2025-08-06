import streamlit as st
import pandas as pd
from models.llm import call_llm
from utils.web_scraper import fetch_moneycontrol_financials
from utils.file_reader import read_financial_files
from utils.rag_retriever import FinancialRAG

st.set_page_config(page_title="FinSightX")
st.title("📊 FinSightX – Analyze Company Financials Intelligently")

# Session state to store history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

mode = st.selectbox("Choose response mode", ["concise", "detailed"])
model = st.selectbox("Choose LLM model", ["groq", "gemini", "deepseek"])

company_name = st.text_input("Enter Company Name (e.g., Infosys)")
uploaded_files = st.file_uploader("Upload Financial Documents (PDF, CSV)", type=["pdf", "csv"], accept_multiple_files=True)
question = st.text_input("Ask something about the financials:")

# Collect all document content
document_chunks = []

if uploaded_files:
    for file in uploaded_files:
        chunks = read_financial_files(file)
        document_chunks.extend(chunks)

elif company_name:
    st.info("🔍 Scraping data from Moneycontrol...")
    dfs = fetch_moneycontrol_financials(company_name)
    if isinstance(dfs, list):
        for df in dfs:
            if isinstance(df, pd.DataFrame):
                document_chunks.append(df.to_string(index=False))
    else:
        st.warning(f"❌ Error: {dfs}")

# Process question
if question and document_chunks:
    rag = FinancialRAG()
    rag.add_chunks(document_chunks)
    context = "\n\n".join(rag.query(question))

    prompt = f"Here is the relevant financial context:\n{context}\n\nUser question: {question}"
    answer = call_llm(prompt)

    # Save the exchange to history
    st.session_state.chat_history.append({"user": question, "bot": answer})

# Show the full conversation
if st.session_state.chat_history:
    st.markdown("### 💬 Chat History")
    for exchange in st.session_state.chat_history:
        st.markdown(f"**You:** {exchange['user']}")
        st.markdown(f"**AI:** {exchange['bot']}")

else:
    st.info("📥 Upload a financial file or enter a company name to begin.")
