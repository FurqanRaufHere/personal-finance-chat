import os
import sys
import streamlit as st

# Add the project root to sys.path to enable imports from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm_client import LLMClient
from src.prompts import get_system_prompt
from src.utils import start_history, append_user, append_assistant, truncate_history

st.set_page_config(page_title="Finance Chat", page_icon="💸", layout="centered")

# Title & disclaimer
st.title("💸 Personal Finance Chatbot")
st.caption("Disclaimer: This chat is for educational purposes only, not financial advice.")

# Sidebar persona selector
persona = st.sidebar.radio("Choose persona:", ["professional", "creative", "technical"])

# Clear chat button
if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []
    system_prompt = get_system_prompt(persona)
    st.session_state.llm_history = start_history(system_prompt)
    st.rerun()

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize LLM history if not exists or persona changed
if "llm_history" not in st.session_state or st.session_state.get("current_persona") != persona:
    system_prompt = get_system_prompt(persona)
    st.session_state.llm_history = start_history(system_prompt)
    st.session_state.current_persona = persona

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input box
if user_input := st.chat_input("Type your question here..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display immediately
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call LLM
    client = LLMClient()
    append_user(st.session_state.llm_history, user_input)
    st.session_state.llm_history = truncate_history(st.session_state.llm_history)
    response = client.chat(st.session_state.llm_history)
    append_assistant(st.session_state.llm_history, response)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(response)

# Export button
if st.session_state.messages:
    transcript = "\n".join(
        f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages
    )
    st.download_button(
        "💾 TXT",
        data=transcript,
        file_name="chat.txt",
        mime="text/plain",
        help="Download chat as text file"
    )
