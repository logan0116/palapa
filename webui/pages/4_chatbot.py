import streamlit as st
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")  # 填写您自己的APIKey

st.title("Chatbot 🤖")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "你是一个用于科研的助手，擅长于从文献分析的角度为用户提供帮助。"},
        {"role": "assistant", "content": "你好！欢迎来到Palapa！"}
    ]
if "model_engine" not in st.session_state:
    st.session_state["model_engine"] = "glm-4-air"

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
            response = client.chat.completions.create(
                model=st.session_state["model_engine"],
                messages=st.session_state.messages
            )
            output = response.choices[0].message.content
        st.markdown(output)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": output})
