import time
from zhipuai import ZhipuAI
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini')

host = config['local_chat']['host']
port = config['local_chat']['port']


def chat(each_prompt: list, local_mode=False):
    """
    example
    :param each_prompt:
    :param local_mode:
    :return:
    """
    if not local_mode:
        client = ZhipuAI(api_key=config['zhipu_chat']['api_key'])
        response = client.chat.completions.create(
            model="glm-4-air",
            messages=each_prompt
        )
        return response.choices[0].message.content
    else:
        # local mode
        url = f"http://{host}:{port}/chat"
        res = requests.post(
            url,
            json={
                "inputs": each_prompt[-1]['content'],
                "history": [{"role": 'system', "content": '你是一个优秀的助手。'}] + each_prompt[:-1]
            },
            timeout=60)
        return res.json()['data']
