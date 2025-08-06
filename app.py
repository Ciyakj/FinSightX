
import streamlit as st
from utils.chat_handler import chat_interface
from utils.web_scraper import get_company_financial_urls, scrape_financial_tables
from utils.file_reader import parse_uploaded_files
from utils.rag_retriever import FinancialRAG
from models.llm import call_llm
import pandas as pd

st.set_page_config(page_title="📊 FinSightX – Financial Analyst Chatbot")

st.title("📊 FinSightX – Analyze Company Financials Intelligently")
mode = st.selectbox("Choose response mode", ["concise", "detailed"])
model = st.selectbox("Choose LLM model", ["groq", "gemini", "deepseek"])

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

company_name = st.text_input("Enter Company Name (e.g., Infosys)")
uploaded_files = st.file_uploader("Upload Financial Documents (PDF, CSV)", accept_multiple_files=True)
question = st.text_input("Ask something about the financials:")

if company_name and question and not uploaded_files:
    st.info("🔍 Searching for company financial data...")
    urls = get_company_financial_urls(company_name)
    tables = scrape_financial_tables(urls)
    context = "\n\n".join([df.to_string(index=False) for df in tables if isinstance(df, pd.DataFrame)])

    rag = FinancialRAG()
    rag.add_chunks(context.split("\n\n"))
    relevant = "\n\n".join(rag.query(question))

    response = call_llm(f"{relevant}\n\nUser Question: {question}", model=model, mode=mode)
    chat_interface(question, response)

elif uploaded_files and question:
    content = parse_uploaded_files(uploaded_files)
    rag = FinancialRAG()
    rag.add_chunks(content.split("\n\n"))
    relevant = "\n\n".join(rag.query(question))

    response = call_llm(f"{relevant}\n\nUser Question: {question}", model=model, mode=mode)
    chat_interface(question, response)

else:
    st.info("Upload a financial file or enter a company name to begin.")
