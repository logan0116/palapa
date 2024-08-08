#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：3_download_pdf.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/26 下午8:39 
"""

import sqlite3
import time
import requests
import os
import sys


def load_pdf_link(cursor):
    """
    从数据库获取所有的pdf链接
    :return:
    """
    # 从数据库获取所有的未read的title和abstract
    cursor.execute('SELECT id, pdf_url FROM papers WHERE deal_status = TRUE')
    pdf_link_list = cursor.fetchall()
    # replace 'Link:'
    id_list = [pdf_link[0] for pdf_link in pdf_link_list]
    pdf_link_list = [pdf_link[1].replace('Link: ', '').strip() for pdf_link in pdf_link_list]
    return id_list, pdf_link_list


def get_download_path(pdf_path):
    """
    获取下载路径
    :return:
    """
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    download_path = os.path.join(pdf_path, local_time)
    # mkdir
    if not os.path.exists(download_path):
        os.mkdir(download_path)
    return download_path


def download_pdf(pdf_link_list, download_path):
    """
    下载pdf
    :param pdf_link_list:
    :return:
    """
    pdf_path_list = []
    for pdf_link in pdf_link_list:
        # pdf_link = 'https://arxiv.org/pdf/2311.12798'
        pdf_name = pdf_link.split('/')[-1]
        pdf_path = os.path.join(download_path, pdf_name+'.pdf')
        # download
        r = requests.get(pdf_link)
        with open(pdf_path, 'wb') as f:
            f.write(r.content)
        print('Download {} successfully.'.format(pdf_name))
        time.sleep(5)
        pdf_path_list.append(pdf_path)
    return pdf_path_list


def update_pdf_path(cursor, id_list, pdf_path_list):
    """
    更新数据库
    :param cursor:
    :param id_list:
    :param pdf_path_list:
    :return:
    """
    for id_, pdf_path in zip(id_list, pdf_path_list):
        cursor.execute("UPDATE papers SET pdf_path = ? WHERE id = ?", (pdf_path, id_))


def main(database_path, pdf_path):
    # database
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(database_path)
    # 创建一个 Cursor:
    cursor = conn.cursor()
    # 从数据库获取所有的pdf链接
    id_list, pdf_link_list = load_pdf_link(cursor)
    # 下载pdf
    print('Start downloading pdf...')
    download_path = get_download_path(pdf_path)
    pdf_path_list = download_pdf(pdf_link_list, download_path)
    # 更新数据库
    print('Start updating database...')
    update_pdf_path(cursor, id_list, pdf_path_list)
    print('Done.')
    cursor.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    database_path = sys.argv[1]
    pdf_path = sys.argv[2]
    main(database_path, pdf_path)
