#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：paper_screen.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/26 下午5:36 
"""

import sqlite3
import requests
import sys


def load_title_abstract(cursor):
    """
    从数据库获取所有的未read的title和abstract
    :return:
    """

    # 从数据库获取所有的未read的title和abstract
    cursor.execute('SELECT title, abstract FROM papers WHERE if_read = FALSE')
    title_abstract_list = cursor.fetchall()

    return title_abstract_list


def get_top(s_list, t_list, num_top):
    """
    get top k by post
    :return:
    """
    try:
        res = requests.post('http://192.168.1.116:9001/get_top',
                            json={"source": s_list, 
                                  "target": t_list, 
                                  "top_k": num_top,
                                  "top_threshold": 0.0})
        res_data = res.json()
        if len(res_data['data']) > 0:
            code = res_data['code']
            return code, res_data['data']
        else:
            return 500, 'not match'
    except Exception as e:
        return 500, str(e)


def update_deal_status(cursor, title_list_top_k):
    """
    更新deal_status状态
    :param cursor:
    :param title_list_top_k:
    :return:
    """
    for title in title_list_top_k:
        cursor.execute("UPDATE papers SET deal_status = TRUE WHERE title = ?", (title,))


def paper_screen(database_path, source_sentences, num_top):
    # database
    # 连接到 SQLite 数据库
    conn = sqlite3.connect(database_path)
    # 创建一个 Cursor:
    cursor = conn.cursor()

    # 从数据库获取所有的未read的title和abstract
    title_abstract_list = load_title_abstract(cursor)
    target_sentences = [title + '.' + abstract for title, abstract in title_abstract_list]

    # 获取top_k
    print('Getting top_k...')
    code, index_list_top_k = get_top(source_sentences, target_sentences, num_top)
    if code != 200:
        print('Failed to get top_k.', index_list_top_k)
        return

    # 1.更新deal_status状态
    print('Updating deal_status...')
    title_list_top_k = [title_abstract_list[i][0] for i in index_list_top_k]
    update_deal_status(cursor, title_list_top_k)
    print('Done.')
    cursor.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    database_path = sys.argv[1]
    source_sentences = [
        'Exploring the latest advancements in large language model fine-tuning, focusing on parameter-efficient methods and their effectiveness in various NLP tasks.',
        'Investigating the role of prompt engineering in enhancing the performance of large language models, including the development of hard and soft prompts for context-specific applications.',
        'Analyzing in-context learning strategies within large language models to improve understanding and application of complex language tasks.',
        'Exploring domain-specific knowledge graph construction techniques and their impact on information retrieval and data integration.',
        'Advancements in knowledge extraction and fusion for building comprehensive knowledge graphs, emphasizing on representation learning and data accuracy.',
        'Investigating the integration of large language models with knowledge graphs for enhanced natural language understanding and reasoning capabilities.'
    ]
    num_top = 5

    paper_screen(database_path, source_sentences, num_top)
