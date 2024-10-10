import streamlit as st
import os
import subprocess
from pathlib import Path
import sys

# 将 tools 目录添加到 sys.path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'tools'))

from tech_daily.paper_crawler import paper_crawler
from tech_daily.paper_screen import paper_screen



# 1. Start crawling papers...
# 2. Start screening papers...
# 3. Start downloading pdfs...
# 4. Start extracting information...
# 5. Start making scripts...

def run_script(script_path, args):
    result = subprocess.run(['python3', script_path] + args, capture_output=True, text=True)
    return result.stdout


# 初始化状态变量
if 'topic' not in st.session_state:
    st.session_state['topic'] = ""
if 'screen_status' not in st.session_state:
    st.session_state['screen_status'] = False
if 'pdf_download_status' not in st.session_state:
    st.session_state['pdf_download_status'] = False
if 'info_extract_status' not in st.session_state:
    st.session_state['info_extract_status'] = False

# path
if 'database_path' not in st.session_state:
    st.session_state['database_path'] = Path(__file__).resolve().parents[2] / 'data/paper_daily.db'
if 'pdf_path' not in st.session_state:
    st.session_state['pdf_path'] = Path(__file__).resolve().parents[2] / 'data/paper/'
if 'script_path' not in st.session_state:
    st.session_state['script_path'] = Path(__file__).resolve().parents[2] / 'data/script/'

if 'paper_info' not in st.session_state:
    st.session_state['paper_info'] = {}

st.title("技术日报")

topic = st.text_input("请输入您感兴趣的主题，如：深度学习、自然语言处理等，用空格分隔")
if topic is not None:
    st.session_state['topic'] = topic

st.header("1.数据爬取")

# 按钮 - 爬取数据
if st.button("爬取数据"):
    with st.spinner("数据爬取中..."):
        paper_info = paper_crawler(st.session_state['database_path'])
        st.session_state['paper_info'] = paper_info

# table
# paper_info: {'title': title_list_new, 'pdf_link': pdf_link_list_new}
if st.session_state['paper_info']:
    st.dataframe(st.session_state['paper_info'], height=400)

st.header("2.数据筛选")
# input num_pdf
num_pdf = st.number_input("请输入需要查看的PDF数量", min_value=1, max_value=10, value=5)
# 按钮 - 筛选数据
if st.button("筛选数据"):
    if not st.session_state['topic']:
        st.error("请先输入主题")
    else:
        with st.spinner("数据筛选中..."):
            paper_screen(st.session_state['database_path'], st.session_state['topic'].split(), num_pdf)
