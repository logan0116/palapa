import streamlit as st
import os
import subprocess
from pathlib import Path


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

st.title("技术日报")

topic = st.text_input("请输入您感兴趣的主题，如：深度学习、自然语言处理等，用空格分隔")
if topic is not None:
    st.session_state['topic'] = topic

st.header("1.数据爬取")

# 按钮 - 爬取数据
if st.button("爬取数据"):
    with st.spinner("数据爬取中..."):
        # 执行脚本 tools/tech_daily/1_paper_crawler.py
        script_path = os.path.join(os.path.dirname(__file__), '../../tools/tech_daily/1_paper_crawler.py')
        output = run_script(script_path, [st.session_state['database_path']])
        st.text_area("脚本输出", output, height=200)

st.header("2.数据筛选")
# input num_pdf
num_pdf = st.number_input("请输入需要查看的PDF数量", min_value=1, max_value=10, value=5)
# 按钮 - 筛选数据
if st.button("筛选数据"):
    if not st.session_state['topic']:
        st.error("请先输入主题")
    else:
        with st.spinner("数据筛选中..."):
            # 执行脚本 tools/tech_daily/2_paper_screening.py
            script_path = os.path.join(os.path.dirname(__file__), '../../tools/tech_daily/2_paper_screen.py')
            output = run_script(script_path,
                                [st.session_state['database_path'], st.session_state['topic'], str(num_pdf)])
            st.text_area("脚本输出", output, height=100)
            st.session_state['screen_status'] = True

st.header("3.下载PDF")
# 按钮 - 下载PDF
if st.button("下载PDF"):
    if not st.session_state['screen_status']:
        st.error("请先筛选数据")
    else:
        with st.spinner("下载PDF中..."):
            # 执行脚本 tools/tech_daily/3_download_pdf.py
            script_path = os.path.join(os.path.dirname(__file__), '../../tools/tech_daily/3_download_pdf.py')
            output = run_script(script_path,
                                [st.session_state['database_path'], st.session_state['pdf_path']])
            st.text_area("脚本输出", output, height=200)
            st.session_state['pdf_download_status'] = True

st.header("4.信息提取")
# 按钮 - 提取信息
if st.button("提取信息"):
    if not st.session_state['pdf_download_status']:
        st.error("请先下载PDF")
    else:
        with st.spinner("信息提取中..."):
            # 执行脚本 tools/tech_daily/4_info_extract.py
            script_path = os.path.join(os.path.dirname(__file__), '../../tools/tech_daily/4_inf_extract.py')
            output = run_script(script_path,
                                [st.session_state['database_path'], st.session_state['script_path']])
            st.text_area("脚本输出", output, height=200)
            st.session_state['info_extract_status'] = True

st.header("5.生成日报")
# 按钮 - 生成脚本
if st.button("生成日报"):
    if not st.session_state['info_extract_status']:
        st.error("请先提取信息")
    else:
        with st.spinner("生成日报中..."):
            # 执行脚本 tools/tech_daily/5_make_script.py
            script_path = os.path.join(os.path.dirname(__file__), '../../tools/tech_daily/5_script_make.py')
            output = run_script(script_path,
                                [st.session_state['script_path']])
            st.text_area("脚本输出", output, height=200)
            st.success("日报生成成功！")
