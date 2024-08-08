import logging
import json
import re
from collections import defaultdict, Counter

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def build_network_paper(paper2info):
    """
    构建论文引用网络
    :param paper2info:
    :return:
    """
    # get doi2title
    doi2title = {info['doi']: title for title, info in paper2info.items()}
    # get doi-citing-doi
    paper_link = []
    for title, info in paper2info.items():
        if 'citation' in info:
            for citation in info['citation'].split(';'):
                doi_citing = citation.split('DOI')[-1].strip()
                if doi_citing in doi2title:
                    paper_link.append((title, doi2title[doi_citing]))

    return paper_link


def build_network_paper2keyword(paper2kw):
    """
    构建论文关键词网络
    :param paper2kw:
    :return:
    """
    paper2keyword = []

    for title, kw in paper2kw.items():
        for keyword in kw:
            paper2keyword.append((title, keyword))
    # filter
    # paper2keyword = [item for item in paper2keyword if item[2] > weight_threshold]

    return paper2keyword


def get_keyword4sentence(sentence, keyword_list):
    """
    获取句子中的关键词及关键词位置
    :param sentence:
    :param keyword_list:
    :return:
    """
    keyword2position = defaultdict(list)
    for keyword in keyword_list:
        if keyword in sentence:
            start_bit = 0
            for i in range(sentence.count(keyword)):
                keyword2position[keyword].append(sentence.find(keyword, start_bit))
                start_bit = sentence.find(keyword, start_bit) + 1

    return keyword2position


def get_keyword2keyword4sentence(keyword2position):
    """
    keyword(subject)-predicate-keyword(object)
    :param keyword2position:
    :return:
    """
    keyword2keyword_temp = []
    keyword2position_len = len(keyword2position)
    for i in range(keyword2position_len - 1):
        for j in range(i + 1, keyword2position_len):
            keyword1, position1_list = list(keyword2position.items())[i]
            keyword2, position2_list = list(keyword2position.items())[j]
            for position1 in position1_list:
                for position2 in position2_list:
                    if position1 < position2:
                        # kw1 -> kw2
                        keyword2keyword_temp.append((keyword1, keyword2))
                    else:
                        # kw2 -> kw1
                        keyword2keyword_temp.append((keyword2, keyword1))

    return keyword2keyword_temp


def build_network_keyword(paper2info, keyword_list, weight_threshold):
    """
    构建关键词网络
    :param paper2info:
    :param keyword_list:
    :param weight_threshold:
    :return:
    """
    keyword_list = [' ' + keyword + ' ' for keyword in keyword_list]
    keyword2keyword = []

    for title, info in paper2info.items():
        sentence_list = [title] + info['abstract'].split('.')
        for sentence in sentence_list:
            sentence = ' ' + sentence + ' '
            sentence = re.sub(r'[^\w\s]', ' ', sentence)
            sentence = sentence.lower()
            keyword2position = get_keyword4sentence(sentence, keyword_list)
            keyword2keyword_temp = get_keyword2keyword4sentence(keyword2position)
            keyword2keyword.extend(keyword2keyword_temp)

    # weighted
    keyword2keyword = [k1.strip() + ' | ' + k2.strip() for k1, k2 in keyword2keyword]
    keyword2keyword = Counter(keyword2keyword)
    keyword2keyword = [k1_k2.split(' | ') + [count] for k1_k2, count in keyword2keyword.items()]
    # filter
    keyword2keyword = [item for item in keyword2keyword if item[2] > weight_threshold]

    return keyword2keyword


def build_network(paper2info, paper2kw, keyword_list, weight_threshold):
    """
    这一阶段需要构建三个网络：
        paper-citing-paper
        paper-has-keyword
        keyword(subject)-predicate-keyword(object)
    :param paper2info:
    :param paper2kw:
    :param keyword_list:
    :param weight_threshold:

    :return:
    """
    paper2paper = build_network_paper(paper2info)
    logging.info("Paper-citing-paper network has been built.")
    logging.info(f"Size: {len(paper2paper)}")
    paper2word = build_network_paper2keyword(paper2kw)
    logging.info(f"Paper-has-keyword network has been built.")
    logging.info(f"Size: {len(paper2word)}")
    word2word = build_network_keyword(paper2info, keyword_list, weight_threshold)
    logging.info(f"Keyword(subject)-predicate-keyword(object) network has been built.")
    logging.info(f"Size: {len(word2word)}")
    return paper2paper, paper2word, word2word


def get_network(task, weight_threshold):
    """
    :param task:
    :param weight_threshold:
    :return:
    """
    with open(f'data/{task}/processed_file/paper2info.json', 'r', encoding='utf-8') as f:
        paper2info = json.load(f)
    with open(f'data/{task}/processed_file/keyword2count.json', 'r', encoding='utf-8') as f:
        kw2count = json.load(f)
    with open(f'data/{task}/processed_file/paper2kw.json', 'r', encoding='utf-8') as f:
        paper2kw = json.load(f)

    # logging num of paper, kw
    logging.info(f"Num of paper: {len(paper2info)}")
    logging.info(f"Num of keyword: {len(kw2count)}")

    keyword_list = list(kw2count.keys())
    paper2paper, paper2word, word2word = build_network(paper2info, paper2kw, keyword_list, weight_threshold)
    # save
    with open(f'data/{task}/processed_file/link_paper2paper.json', 'w', encoding='utf-8') as f:
        json.dump(paper2paper, f, ensure_ascii=False, indent=4)
    with open(f'data/{task}/processed_file/link_paper2word.json', 'w', encoding='utf-8') as f:
        json.dump(paper2word, f, ensure_ascii=False, indent=4)
    with open(f'data/{task}/processed_file/link_word2word.json', 'w', encoding='utf-8') as f:
        json.dump(word2word, f, ensure_ascii=False, indent=4)

    return len(paper2paper), len(paper2word), len(word2word)
