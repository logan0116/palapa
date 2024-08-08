import streamlit as st
from pathlib import Path
from zhipuai import ZhipuAI

client = ZhipuAI(api_key="")  # 填写您自己的APIKey

st.title("Title Translator")
st.write("这是一个标题翻译器，可以将标题抽象化")

if 'title' not in st.session_state:
    st.session_state['title'] = ""
if "model_engine" not in st.session_state:
    st.session_state["model_engine"] = "glm-4-air"

title = st.text_input("请输入标题")
if title is not None:
    st.session_state['title'] = title

for step_index in range(1, 4):
    if f'prompt_step{step_index}' not in st.session_state:
        prompt_step1_path = Path(__file__).resolve().parents[2] / f'tools/title_translator/prompt/step{step_index}.txt'
        with open(prompt_step1_path, 'r', encoding='utf-8') as f:
            st.session_state[f'prompt_step{step_index}'] = f.read()

if 'elements' not in st.session_state:
    st.session_state['elements'] = []
if 'elements_plus' not in st.session_state:
    st.session_state['elements_plus'] = []

# 这是一个乐子功能
if st.button("翻译"):
    if not st.session_state['title']:
        st.error("请先输入标题")
    else:
        st.write("标题：", st.session_state['title'])
        # 1.要素提取
        st.write(":one: 要素提取")
        with st.spinner("要素提取..."):
            response = client.chat.completions.create(
                model=st.session_state["model_engine"],
                messages=[
                    {"role": "user", "content": st.session_state['prompt_step1'] + st.session_state['title']}
                ]
            )
            output = response.choices[0].message.content
            elements = output.split(' | ')
        # add to st
        st.session_state['elements'] = elements
        # display
        cols = st.columns(len(elements))
        for index, element in enumerate(elements):
            cols[index].write(element)
        # 2.要素转换
        st.write(":two: 要素转换")
        with st.spinner("要素转换..."):
            elements_plus = []
            for element in elements:
                response = client.chat.completions.create(
                    model=st.session_state["model_engine"],
                    messages=[
                        {"role": "user", "content": st.session_state['prompt_step2'] + element + '->'}
                    ]
                )
                output = response.choices[0].message.content
                elements_plus.append(output)
        # add to st
        st.session_state['elements_plus'] = elements_plus
        # display
        cols = st.columns(len(elements_plus))
        for index, element_plus in enumerate(elements_plus):
            cols[index].write(element_plus)
        # 3.要素合成
        st.write(":three: 要素合成")
        with st.spinner("要素合成..."):
            response = client.chat.completions.create(
                model=st.session_state["model_engine"],
                messages=[
                    {"role": "user",
                     "content": st.session_state['prompt_step3'] +
                                '\n标题：' + st.session_state['title'] +
                                '\n要素：' + ' | '.join(elements) +
                                '\n抽象化的要素：' + ' | '.join(elements_plus) +
                                '\n新标题：'}
                ]
            )
            output = response.choices[0].message.content
        # display
        st.write(output)
