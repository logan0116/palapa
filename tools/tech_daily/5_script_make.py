#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：Daily_NLP 
@File    ：5_script_make.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/27 上午12:10 
"""

from openai import OpenAI
import openai
import time
import json
from utils import text_generation
import sys
import os


def load_prompt():
    # load prompt
    with open('prompt/system_prompt.txt', 'r', encoding='utf-8') as f:
        system_prompt = f.read()

    return system_prompt


def export_script(script_path, title_list, response_list, url_list, local_time):
    """
    输出脚本
    :param title_list:
    :param response_list:
    :param url_list:
    :param local_time:
    :return:
    """
    start = '嗨，欢迎来到今天的NLP资讯速递，让我们看看又有哪些最新的研究。\n\n'
    end = '以上是今天所有的内容，如果您对今天讨论的任何主题感兴趣，不妨深入阅读相关论文，以获取更全面的了解。祝你今天有个好心情~ '

    script_text_output_path = os.path.join(script_path, local_time, 'outputs.txt')
    with open(script_text_output_path, 'w', encoding='utf-8') as f:
        f.write(start)
        for index, (title, response, url) in enumerate(zip(title_list, response_list, url_list)):
            f.write('## '.format(index + 1) + title + '\n')
            # 介绍
            f.write(response + '\n')
            # pdf link
            f.write('Pdf Link: ' + url + '\n\n')
        f.write(end + '\n')


def make_prompt_research(prompt, title, abstract, context):
    each_prompt = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"Title: {title}\nAbstract: {abstract}\nContext: {context}"},
        {"role": "assistant", "content": ''}
    ]
    return each_prompt


def make_script(script_path):
    local_time = time.strftime("%Y-%m-%d", time.localtime())
    script_text_input_path = os.path.join(script_path, local_time, 'inputs.json')

    with open(script_text_input_path, 'r', encoding='utf-8') as f:
        paper_info_list = json.load(f)
    response_list = []

    # load prompt
    system_prompt = load_prompt()

    for title_abstract in paper_info_list:
        # response
        title, abstract, context = title_abstract['title'], title_abstract['abstract'], title_abstract['context']
        each_prompt = make_prompt_research(system_prompt, title, abstract, context)
        message = text_generation(each_prompt, mode='deepseek')
        response_list.append(message.strip())

    title_list = [title_abstract['title'] for title_abstract in paper_info_list]
    url_list = [title_abstract['pdf_url'] for title_abstract in paper_info_list]

    export_script(script_path, title_list, response_list, url_list, local_time)
    print('Script has been generated successfully!')


if __name__ == '__main__':
    # script_path = sys.argv[1]
    script_path = '../../data/script/'
    make_script(script_path)
