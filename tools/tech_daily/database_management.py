#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：database_management.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/26 下午3:30 
"""

import sqlite3

# 连接到 SQLite 数据库
conn = sqlite3.connect('../../data/paper_daily.db')

# 创建一个 Cursor:
cursor = conn.cursor()

# 删除现有的表（如果存在）
cursor.execute('DROP TABLE IF EXISTS papers')
cursor.execute('DROP TABLE IF EXISTS authors')
cursor.execute('DROP TABLE IF EXISTS paper_author')

# 创建 总文献表
cursor.execute('''CREATE TABLE papers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    abstract TEXT,
                    pdf_url TEXT,
                    pdf_path TEXT,
                    date TEXT,
                    deal_status BOOLEAN,
                    if_read BOOLEAN
                )''')

# 创建 作者表
cursor.execute('''CREATE TABLE authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    info_url TEXT
                )''')

# 创建 作者-文献关联表
cursor.execute('''CREATE TABLE paper_author (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_id INTEGER,
                    paper_id INTEGER,
                    FOREIGN KEY (author_id) REFERENCES authors(id),
                    FOREIGN KEY (paper_id) REFERENCES papers(id)
                )''')

# 关闭 Cursor:
cursor.close()

# 提交事务:
conn.commit()

# 关闭 Connection:
conn.close()
