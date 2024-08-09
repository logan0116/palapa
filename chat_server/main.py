#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fd_backend_alarm_match 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/29 下午4:11 
"""
# llama
from llama_cpp import Llama
# fastapi
import uvicorn
from fastapi import FastAPI
# local
from model import ChatReqItem, ChatResItem
from parser import parameter_parser

args = parameter_parser()

app = FastAPI()

# load model
llm = Llama(
    model_path=args.model_path,
    n_gpu_layers=100,  # Uncomment to use GPU acceleration
    n_ctx=args.n_ctx,  # Uncomment to increase the context window
)


@app.post("/chat")
async def my_chat(query_info: ChatReqItem):
    """
    获取句子的embedding
    :param query_info:
    :return:
    """
    inputs = query_info.inputs
    history = query_info.history

    # add history
    if history:
        history.append({'role': 'user', 'content': inputs})

    # output
    try:
        output = llm.create_chat_completion(
            messages=history,
            max_tokens=2048,
            temperature=0.7)
        output = output['choices'][0]['message']['content'].strip()
        return ChatResItem(code=200, msg="success", data=output)
    except Exception as e:
        return ChatResItem(code=500, msg="chat server error", data=str(e))


if __name__ == '__main__':
    uvicorn.run(app=app,
                host='0.0.0.0',
                port=args.port,
                workers=1)
