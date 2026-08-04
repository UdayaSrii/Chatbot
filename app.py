import os
from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
st.set_page_config(page_title="AI Chatbot", page_icon="", layout="centered")
st.title("AI Chatbot using LangChain +Groq")
if not api_key:
    st.error("GROQ_API_KEY not found. Create a .env file with:\n\nGROQ_API_KEY=your_api_key")
    st.stop()
temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.2, 0.1)
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=temperature,
    api_key=api_key
)
if "messages" not in st.session_state:
    st.session_state.messages = []
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)
prompt = st.chat_input("Ask me anything...")
if prompt:
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = llm.invoke(prompt).content
            st.markdown(response)
    st.session_state.messages.append(("assistant", response))
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    st.rerun()