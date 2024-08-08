import os
import json
from tqdm import tqdm


class PaperSet:
    def __init__(self, task, file_list):
        self.task = task
        self.csv_file_list = file_list
        # paper2info
        self.paper2info = {}
        # paper2doc
        self.paper2doc = {}

    def extract_paper_info(self):
        """
        整理所有的paper信息
        :return:
        """
        for csv in tqdm(self.csv_file_list):
            self.get_paper_inf4each_cev(csv)

    def get_paper_inf4each_cev(self, uploaded_file):
        """
        获取paper中的信息
        从wos中下载的csv文件中
        1.title TI
        2.abstract AB
        3.time PY
        4.doi DI
        5.journal SO
        6.keywords DE
        7.citation CR
        :return:
        """
        # deal
        data = uploaded_file.read().decode('utf-8').splitlines()
        head_list = data[0].split('\t')
        index_list = [head_list.index(i) for i in ['TI', 'AB', 'PY', 'DI', 'SO', 'DE', 'CR']]
        for paper in data[1:]:
            paper_info = paper.split('\t')
            title = paper_info[index_list[0]]
            abstract = paper_info[index_list[1]]
            time = paper_info[index_list[2]]
            doi = paper_info[index_list[3]]
            journal = paper_info[index_list[4]]
            keywords = paper_info[index_list[5]]
            citation = paper_info[index_list[6]]

            self.paper2info[title] = {'abstract': abstract,
                                      'time': time,
                                      'doi': doi,
                                      'journal': journal,
                                      'keywords': keywords,
                                      'citation': citation}

            self.paper2doc[title] = abstract

    def save(self):
        # 创建路径 在../../data/路径下
        if not os.path.exists(f'data/{self.task}/processed_file'):
            os.makedirs(f'data/{self.task}/processed_file')

        with open(f'data/{self.task}/processed_file/paper2info.json', 'w', encoding='utf-8') as f:
            json.dump(self.paper2info, f, ensure_ascii=False, indent=4)
        with open(f'data/{self.task}/processed_file/paper2doc.json', 'w', encoding='utf-8') as f:
            json.dump(self.paper2doc, f, ensure_ascii=False, indent=4)


def get_paper_info(task, file_list):
    """
    提取文件信息
    :param task:
    :param file_list:
        from st.file_uploader
    :return:
    """
    paper_set = PaperSet(task, file_list)
    paper_set.extract_paper_info()
    paper_set.save()
    return len(paper_set.paper2info)
