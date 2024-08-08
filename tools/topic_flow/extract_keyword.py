import requests
import json

import logging
import time
from tqdm import tqdm
from collections import Counter

from .redis_model import RedisQueue, RedisDict

# logging config
logging.basicConfig(level=logging.INFO,
                    format="Logan233: %(asctime)s %(levelname)s [%(name)s] %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")

# # 初始化队列和字典
queue_inputs = RedisQueue('queue_inputs', maxsize=32)
dict_outputs = RedisDict('dict_outputs', maxsize=32)

queue_inputs.clear()
dict_outputs.clear()


def extract_keyword_entity(paper2doc):
    """
    通过大语言模型提取关键词
    model: LLaMA3
    :param paper2doc:
    :return:
    """
    # load prompt
    role_prompt_path = "prompt/prompt_keyword_extract.txt"
    with open(role_prompt_path, 'r', encoding='utf-8') as f:
        role_prompt = f.read()
    # load example
    example_path = "prompt/example_keyword_extract.json"
    with open(example_path, 'r', encoding='utf-8') as f:
        example = json.load(f)
    # history
    history = [{"role": "system", "content": role_prompt}] + example

    # start.sh time
    logging.info(f"Start extracting keyword...")

    # result
    paper2kw = {}

    index_enqueue = 0
    index_dequeue = 0
    try:
        while True:
            if len(paper2doc) == len(paper2kw):
                break

            while index_enqueue < index_dequeue + 12 and index_enqueue < len(paper2doc):
                title, abstract = list(paper2doc.items())[index_enqueue]
                prompt = "Title: " + title + "\nAbstract: " + abstract
                queue_inputs.enqueue(id_=title, inputs=prompt, history=history)
                logging.info(f"Enqueue: {index_enqueue}")
                index_enqueue += 1

            if dict_outputs.size() > 6 or index_enqueue == len(paper2doc):
                title_list_temp = dict_outputs.get_keys()
                for title in title_list_temp:
                    output = dict_outputs.get(title).decode('utf-8')
                    logging.info(f"Dequeue: {index_dequeue}")
                    index_dequeue += 1
                    keyword_list = output.split(" | ")
                    paper2kw[title] = keyword_list
                    dict_outputs.delete(title)
                    paper2kw[title] = keyword_list

    except BaseException as e:
        print(str(e))
        return paper2kw

    return paper2kw


def get_keyword_advanced(task):
    """
    两个来源
        2. 大模型提取的关键词
    :param task:
    :return:
    """
    # load paper2doc
    with open(f'data/{task}/processed_file/paper2doc.json', 'r', encoding='utf-8') as f:
        paper2doc = json.load(f)
    # extract keyword
    paper2kw = extract_keyword_entity(paper2doc)
    with open(f'data/{task}/processed_file/paper2kw.json', 'w', encoding='utf-8') as f:
        json.dump(paper2kw, f, ensure_ascii=False, indent=4)


def kw_list_clean(kw_list):
    """
    clean lower, strip
    :param kw_list:
    :return:
    """
    kw_list = [kw.lower().strip() for kw in kw_list]
    kw_list = [kw for kw in kw_list if kw != '']
    return kw_list


def get_keyword(task,word_freq):
    """
    两个来源
        1. 论文的作者关键词
    :return:
    """
    # load paper2info
    with open(f'data/{task}/processed_file/paper2info.json', 'r', encoding='utf-8') as f:
        paper2info = json.load(f)

    paper2kw = {}
    kw_list = []
    for title, info in paper2info.items():
        kw_list_temp = info['keywords'].split(';')
        kw_list_temp = kw_list_clean(kw_list_temp)
        paper2kw[title] = kw_list_temp
        kw_list.extend(kw_list_temp)
    # count
    keyword2count = Counter(kw_list)
    # clean by freq
    keyword2count = {kw: count for kw, count in keyword2count.items() if count > word_freq}
    keyword_set = set(keyword2count.keys())
    paper2kw_clean = {}
    for paper, kw in paper2kw.items():
        paper2kw_clean[paper] = list(set(kw) & keyword_set)

    # save
    with open(f'data/{task}/processed_file/keyword2count.json', 'w', encoding='utf-8') as f:
        json.dump(keyword2count, f, ensure_ascii=False, indent=4)
    with open(f'data/{task}/processed_file/paper2kw.json', 'w', encoding='utf-8') as f:
        json.dump(paper2kw, f, ensure_ascii=False, indent=4)

    return len(keyword2count)
