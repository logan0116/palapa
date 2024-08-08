import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# 将 tools 目录添加到 sys.path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'tools'))

from topic_flow.paper_info import get_paper_info
from topic_flow.extract_keyword import get_keyword, get_keyword_advanced
from topic_flow.build_network import get_network

# 分为四个大的步骤
# 1.数据处理
# 2.特征提取
# 3.主题聚类
# 4.主题演化

# 初始化状态变量
if 'file_path' not in st.session_state:
    st.session_state['file_path'] = []
if 'task' not in st.session_state:
    st.session_state['task'] = ""
if 'paper_info_status' not in st.session_state:
    st.session_state['paper_info_status'] = False
if 'num_paper' not in st.session_state:
    st.session_state['num_paper'] = 0
if 'keyword_status' not in st.session_state:
    st.session_state['keyword_status'] = False
if 'num_keyword' not in st.session_state:
    st.session_state['num_keyword'] = 0
if 'network_status' not in st.session_state:
    st.session_state['network_status'] = False
if 'num_paper2paper' not in st.session_state:
    st.session_state['num_paper2paper'] = 0
if 'num_paper2keyword' not in st.session_state:
    st.session_state['num_paper2keyword'] = 0
if 'num_keyword2keyword' not in st.session_state:
    st.session_state['num_keyword2keyword'] = 0

st.title("主题流动分析")

task = st.text_input("请输入任务名称")
if task is not None:
    st.session_state['task'] = task

st.header("1.数据处理")

st.subheader("1.1 读取文件")
uploaded_files = st.file_uploader("请选择来自Web of Science的CSV文件",
                                  type='csv',
                                  accept_multiple_files=True)
if uploaded_files is not None:
    st.session_state['file_path'] = uploaded_files

# 按钮 - 提取文件
if st.button("提取文件"):
    if not st.session_state['file_path']:
        st.error("请先选择文件")
    elif not st.session_state['task']:
        st.error("请先输入任务名称")
    else:
        with st.spinner("文件提取中"):
            st.session_state['num_paper'] = get_paper_info(st.session_state['task'], st.session_state['file_path'])
        st.session_state['paper_info_status'] = True
        st.success("文件提取完成，共提取文件数：{}".format(st.session_state['num_paper']))

# 拆分两列 提取关键词-base 提取关键词-advanced columns
st.subheader("1.2 提取关键词")

col1, col2 = st.columns(2)
with col1:
    st.write("**提取关键词-基础版**")
    st.write("根据论文的作者关键词提取，可设置关键词频率阈值")
    # word freq
    word_freq = st.number_input("word freq", 1)
    # 按钮 - 提取关键词-base
    if st.button("提取关键词"):
        if not st.session_state['paper_info_status']:
            st.error("请先提取文件")
        else:
            with st.spinner("关键词提取中"):
                st.session_state['num_keyword'] = get_keyword(st.session_state['task'], word_freq)
            st.session_state['keyword_status'] = True
            st.success("关键词提取完成，共提取关键词数：{}".format(st.session_state['num_keyword']))

with col2:
    # 按钮 - 提取关键词-advanced
    st.write("**提取关键词-高级版**")
    st.write("根据大模型提取的关键词")
    st.write("coming soon...")

st.subheader("1.3 构建网络")
st.write("对三类关系进行网络构建：")
st.write("1. Paper-citing-paper")
st.write("2. Paper-has-keyword")
st.write("3. Keyword(subject)-predicate-keyword(object) （需要权重约束）")
# weight4kw2kw
weight_threshold = st.number_input("weight threshold for keyword2keyword", 5)

# 按钮 - 构建网络
if st.button("构建网络"):
    if not st.session_state['keyword_status']:
        st.error("请先提取关键词")
    else:
        with st.spinner("网络构建中"):
            num_list = get_network(st.session_state['task'], weight_threshold)
            st.session_state['num_paper2paper'] = num_list[0]
            st.session_state['num_paper2keyword'] = num_list[1]
            st.session_state['num_keyword2keyword'] = num_list[2]
        st.session_state['network_status'] = True
        st.success("网络构建完成")

# 表格
# header: num_paper, num_keyword, num_paper2paper, num_paper2keyword, num_keyword2keyword
df = pd.DataFrame({
    "paper": [st.session_state['num_paper']],
    "keyword": [st.session_state['num_keyword']],
    "paper2paper": [st.session_state['num_paper2paper']],
    "paper2keyword": [st.session_state['num_paper2keyword']],
    "keyword2keyword": [st.session_state['num_keyword2keyword']]
}, index=['num'])
st.table(df)

st.header("2.特征提取")

st.header("3.主题聚类")

st.header("4.主题演化")
