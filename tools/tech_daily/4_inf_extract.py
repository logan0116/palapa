#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：4_inf_extract.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/26 下午9:52 
"""
import json
import sqlite3
import time
import pdfplumber
import os
import sys


def get_info(cursor):
    """
    从数据库获取所有的未read的title和abstract
    :return:
    """
    # 从数据库获取所有的未read的title和abstract
    cursor.execute('SELECT id, title, abstract, pdf_path,pdf_url FROM papers  WHERE deal_status = TRUE')
    info_list = cursor.fetchall()
    id_list = [info[0] for info in info_list]
    title_list = [info[1] for info in info_list]
    abstract_list = [info[2] for info in info_list]
    pdf_path_list = [info[3] for info in info_list]
    pdf_url_list = [info[4] for info in info_list]

    return id_list, title_list, abstract_list, pdf_path_list, pdf_url_list


def get_script_save_path(script_path):
    """
    获取下载路径
    :return:
    """
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    script_save_path = os.path.join(script_path, local_time)
    # mkdir
    if not os.path.exists(script_save_path):
        os.mkdir(script_save_path)
    return script_save_path


def save_title_abstract(title_list, abstract_list, context_list, pdf_url_list, script_save_path):
    """
    保存title和abstract
    :param title_list:
    :param abstract_list:
    :param context_list:
    :param pdf_url_list:
    :param script_save_path:
    :return:
    """
    paper_info_list = []
    for title, abstract, context, pdf_url in zip(title_list, abstract_list, context_list, pdf_url_list):
        paper_info = {
            'title': title,
            'abstract': abstract,
            'context': context,
            'pdf_url': pdf_url
        }
        paper_info_list.append(paper_info)

    with open(os.path.join(script_save_path, 'inputs.json'), 'w', encoding='utf-8') as f:
        json.dump(paper_info_list, f, ensure_ascii=False, indent=4)


def get_info_from_pdf(pdf_path_list):
    """
    提取文本 based on pdfplumber
        主要目的是提取pdf中的introduction部分
    :param pdf_path_list:
    :return:
    """
    text_list = []
    for pdf_path in pdf_path_list:
        text = ''
        with pdfplumber.open(pdf_path) as pdf:
            for i in range(min(3, len(pdf.pages))):
                page = pdf.pages[i]
                text += page.extract_text()

        if 'Introduction' in text:
            text = text[text.index('Introduction') + len('Introduction'):]

        text_list.append(text.strip())

    return text_list


def update_deal_read_status(cursor, id_list):
    """
    deal_status = FALSE
    if_read = TRUE
    :param cursor:
    :param id_list:
    :return:
    """
    for id_ in id_list:
        cursor.execute("UPDATE papers SET deal_status = FALSE, if_read = TRUE WHERE id = ?", (id_,))


def main(database_path, script_path):
    # database
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(database_path)
    # 创建一个 Cursor:
    cursor = conn.cursor()
    # 创建一个路径，用于存放提取的信息
    script_save_path = get_script_save_path(script_path)
    # 从数据库获取所有deal_status为TRUE的title和abstract和pdf_path
    id_list, title_list, abstract_list, pdf_path_list, pdf_url_list = get_info(cursor)
    # get image from pdf
    context_list = get_info_from_pdf(pdf_path_list)
    # 保存title和abstract
    save_title_abstract(title_list, abstract_list, context_list, pdf_url_list, script_save_path)
    # 更新数据库
    print('Start updating database...')
    update_deal_read_status(cursor, id_list)
    print('Done.')
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    database_path = sys.argv[1]
    script_path = sys.argv[2]
    main(database_path, script_path)
