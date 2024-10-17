import re

import streamlit as st
import os
import subprocess
from pathlib import Path
import sys

# 将 tools 目录添加到 sys.path
sys.path.append(str(Path(__file__).resolve().parents[2] / 'tools'))


# 读取文件
def load_data():
    """
    获取所有的日报信息
    """
    data_path = 'data/summary'
    date_file_path = os.listdir(data_path)
    # sort by date
    date_list = sorted(date_file_path, key=lambda x: int(x.replace('-', '')), reverse=True)

    date2summary = {}
    for date in date_list:
        with open(os.path.join(data_path, date, "outputs.md"), 'r', encoding='utf-8') as f:
            date2summary[date] = f.read()
    return date2summary


date2summary = load_data()

# 侧边栏展示所有的日报
date = st.sidebar.selectbox("选择日期", list(date2summary.keys()))


# split by img
def split_by_img(summary):
    """
    将日报内容按照图片分割
    """
    # re
    pattern = re.compile(r'!\[.*?\.png]\(.*?\.png\)')
    summary_part_list = pattern.split(summary)
    img_list = pattern.findall(summary)
    # img_list clean
    img_list_clean = []
    for img in img_list:
        img = re.search(r"\(.*?\)", img).group()
        img = img[1:-1]
        pdf_name, img_name = img.split('%2F')[-2:]
        img_list_clean.append(f"data/img/{date}/{pdf_name}/{img_name}")

    return summary_part_list, img_list_clean


summary_part_list, img_list = split_by_img(date2summary[date])

for summary_part, img in zip(summary_part_list[:-1], img_list):
    st.markdown(summary_part)
    # 图片居中
    st.image(img, use_column_width=True)

st.markdown(summary_part_list[-1])
