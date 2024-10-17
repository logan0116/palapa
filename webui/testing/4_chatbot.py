import streamlit as st
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).resolve().parents[2] / 'tools'))

from utils import chat

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个用于科研的助手，擅长于从文献分析的角度为用户提供帮助。"},
        {"role": "assistant", "content": "你好！欢迎来到Palapa！"}
    ]

# Display chat messages from history on app rerun
for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            output = chat(
                each_prompt=st.session_state.messages,
                local_mode=True
            )
        st.markdown(output)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": output})
