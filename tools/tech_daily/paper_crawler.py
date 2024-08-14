#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：paper_crawler.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/26 下午3:38 
"""

import requests
from bs4 import BeautifulSoup
from texttable import Texttable
import sqlite3
import time
import re
import sys


def print_table(table: list, header: list):
    """
    打印表格
    :param table:
    :return:
    """
    t = Texttable()
    t.add_row(header)
    for inf in table:
        t.add_row(inf)
    print(t.draw())


def get_author_info(soup):
    author_dict = {}  # author:link
    author_list = []

    # authors
    for item in soup.select('.list-authors'):
        author_list_temp = []
        for author in item.select('a'):
            author_link = author['href']
            author_name = author.string.strip()
            author_dict[author_name] = author_link
            author_list_temp.append(author_name)
        author_list.append(author_list_temp)

    return author_dict, author_list


def get_pdf_link(soup):
    """
    <dt data-vivaldi-translated="">
      <a name="item1" data-vivaldi-translated="">[1]</a>
      <a href="/abs/2405.03695" title="Abstract" id="2405.03695" data-vivaldi-translated="">arXiv:2405.03695</a>
      <a href="/pdf/2405.03695" title="Download PDF" id="pdf-2405.03695" aria-labelledby="pdf-2405.03695" data-vivaldi-translated="">pdf</a>,
      <a href="/ps/2405.03695" title="Download PostScript" id="ps-2405.03695" aria-labelledby="ps-2405.03695" data-vivaldi-translated="">ps</a>, <a href="/format/2405.03695" title="Other formats" id="oth-2405.03695" aria-labelledby="oth-2405.03695" data-vivaldi-translated="">other</a>]
    </dt>


    :param soup:
    :return:
    """
    pdf_link_list = []
    for item in soup.find_all('dt'):
        links = item.find_all('a', title="Download PDF")
        if links:
            pdf_link = links[0]['href']  # Assume the first link with title "Download PDF" is the correct one.
            pdf_link_list.append(f'https://arxiv.org{pdf_link}')
    return pdf_link_list


def get_title(soup):
    # <div class="list-title mathjax">
    # <span class="descriptor">Title:</span> Frequency Analysis with Multiple Kernels and Complete Dictionary
    # </div>

    title_list = []
    for item in soup.select('.list-title.mathjax'):
        title = item.text.strip()
        if 'Title:' in title:
            title = title.replace('Title:', '').strip()
        title_list.append(title)
    return title_list


def get_abstract(soup):
    abstract_list = []
    # 获取每个论文项目的容器
    for item in soup.select('.meta'):
        # 检查是否存在摘要的段落
        abstract = item.find('p', class_='mathjax')
        if abstract:
            # 使用.strip()来去除多余的空白字符
            abstract_text = abstract.get_text(separator=' ', strip=True)
        else:
            # 如果没有找到摘要，添加一个空字符串作为占位符
            abstract_text = ''
        abstract_list.append(abstract_text)
    return abstract_list


def insert_data(database_path, title_list, abstract_list, pdf_link_list, authors_list, author_dict):
    """
    将数据插入数据库
    :param title_list:
    :param abstract_list:
    :param pdf_link_list:
    :param authors_list:
    :param author_dict:
    :return:
    """
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    local_date = time.strftime("%Y-%m-%d", time.localtime())

    title_list_new = []
    pdf_link_list_new = []

    for title, abstract, pdf_link, authors in zip(title_list, abstract_list, pdf_link_list, authors_list):
        # 检查title是否已存在
        cursor.execute("SELECT id FROM papers WHERE title = ?", (title,))
        paper_record = cursor.fetchone()
        if paper_record:
            # already exist
            paper_id = paper_record[0]

        else:
            # 插入新的论文
            cursor.execute(
                "INSERT INTO papers (title, abstract, pdf_url, pdf_path, date, deal_status, if_read) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (title, abstract, pdf_link, '', local_date, False, False))
            paper_id = cursor.lastrowid

            # add to new list
            title_list_new.append(title)
            pdf_link_list_new.append(pdf_link)

        for author in authors:
            # 检查作者是否已存在
            cursor.execute("SELECT id FROM authors WHERE name = ?", (author,))
            author_record = cursor.fetchone()
            if author_record:
                author_id = author_record[0]
            else:
                # 插入新的作者
                cursor.execute("INSERT INTO authors (name, info_url) VALUES (?, ?)",
                               (author, author_dict[author]))
                author_id = cursor.lastrowid

            # 插入作者和论文的关联
            cursor.execute("INSERT INTO paper_author (author_id, paper_id) VALUES (?, ?)",
                           (author_id, paper_id))

    # 关闭 Cursor:
    cursor.close()

    # 提交事务:
    conn.commit()

    # 关闭 Connection:
    conn.close()

    # print new
    # # 打印表格
    # local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # print('New papers in database at {}:'.format(local_time))
    # print_table(zip([i + 1 for i in range(len(title_list))], title_list_new, pdf_link_list_new),
    #             header=['Index', 'Title', 'PDF Link'])
    return {'title': title_list_new, 'pdf_link': pdf_link_list_new}


def paper_crawler(database_path):
    # arXiv的NLP相关论文列表的URL（这里需要替换为实际的URL）
    url = 'https://arxiv.org/list/cs/new'

    # 发送请求
    response = requests.get(url)
    response.raise_for_status()  # 确保请求成功

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    title_list, authors_list, pdf_link_list, abstract_list = [], [], [], []
    author_dict = {}

    for tag in ['New submissions', 'Cross']:
        # 定位到New submissions的<h3>标签
        h3_tag = soup.find('h3', string=re.compile(tag))
        # 需要的论文信息在<h3>标签上一级的<dl>中
        soup_sub = h3_tag.find_parent('dl')
        # 获取论文标题
        title_list_temp = get_title(soup_sub)
        # add
        title_list.extend(title_list_temp)
        # 获取论文作者
        author_dict_temp, authors_list_temp = get_author_info(soup_sub)
        # add
        author_dict.update(author_dict_temp)
        authors_list.extend(authors_list_temp)
        # 获取论文PDF链接
        pdf_link_list_temp = get_pdf_link(soup_sub)
        # add
        pdf_link_list.extend(pdf_link_list_temp)
        # 获取论文摘要
        abstract_list_temp = get_abstract(soup_sub)
        # add
        abstract_list.extend(abstract_list_temp)

    # print('Title:', len(title_list))
    # print('Authors:', len(authors_list))
    # print('PDF Link:', len(pdf_link_list))
    # print('Abstract:', len(abstract_list))

    # 将数据插入数据库
    paper_info = insert_data(database_path, title_list, abstract_list, pdf_link_list, authors_list, author_dict)
    return paper_info
