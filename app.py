import os
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Load environment variables for local development
load_dotenv()


# Get Groq API Key
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = os.getenv("GROQ_API_KEY")


# Streamlit page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="centered"
)


# Title
st.title("🤖 AI Chatbot using LangChain + Groq")


# Check API Key
if not api_key:
    st.error(
        "GROQ_API_KEY not found.\n\n"
        "For local use create a .env file:\n\n"
        "GROQ_API_KEY=your_api_key\n\n"
        "For Streamlit Cloud add it in:\n\n"
        "App Settings → Secrets"
    )
    st.stop()


# Sidebar settings
st.sidebar.title("⚙️ Settings")

temperature = st.sidebar.slider(
    "Creativity (Temperature)",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.1
)


# Initialize Groq model
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=temperature,
    api_key=api_key
)


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# Chat input
prompt = st.chat_input("Ask me anything...")


if prompt:

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )


    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):

            try:
                response = llm.invoke(prompt).content

            except Exception as e:
                response = f"❌ Error: {str(e)}"

            st.markdown(response)


    # Save AI response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# Clear chat button
if st.sidebar.button("🗑️ Clear Chat"):

    st.session_state.messages = []

    st.rerun()
