
import streamlit as st

def chat_interface(question, response):
    st.session_state.chat_history.append(("user", question))
    st.session_state.chat_history.append(("ai", response))

    for role, msg in st.session_state.chat_history:
        if role == "user":
            st.markdown(f"**You:** {msg}")
        else:
            st.markdown(f"**AI:** {msg}")
