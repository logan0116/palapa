#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fd_backend_alarm_match 
@File    ：main.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/29 下午4:11 
"""
# fastapi
import uvicorn
from fastapi import FastAPI
# model
from FlagEmbedding import BGEM3FlagModel
# base
import torch
# local
from parser import parameter_parser
from model import *

TRANSFORMER_OFFLINE = 1

# 全局变量
args = parameter_parser()
print('load model...')
# model
model = BGEM3FlagModel('BAAI/bge-m3', use_fp16=True, device='cuda:0')
print('load model successfully.')
app = FastAPI()


@app.post("/get_top")
async def get_top_index(search_info: GetTopReqItem):
    """
    request body:
        source: List[str]
        target: List[str]
        top_k: int = 5
        top_threshold: float = 0.75
    """

    s_list = search_info.source
    t_list = search_info.target
    top_k = search_info.top_k
    top_threshold = search_info.top_threshold

    sentence_pairs = [(i, j) for i in s_list for j in t_list]
    try:
        sim = model.compute_score(
            sentence_pairs,
            batch_size=args.batch_size,
            max_passage_length=args.max_passage_length,  # a smaller max length leads to a lower latency
        )
        sim = sim['colbert+sparse+dense']
    except Exception as e:
        return GetTopResItem(code=500, msg=str(e), data=[])

    # reshape output:[num_source * num_target] -> [num_source, num_target]
    sim = torch.tensor(sim).reshape(len(s_list), len(t_list))
    # mean pooling output:[num_source, num_target] -> [num_target]
    sim = sim.mean(dim=0)
    _, sim_index = torch.sort(sim, descending=True)
    # top_k_threshold
    sim = sim.numpy().tolist()
    sim_index = sim_index.numpy().tolist()
    top_k_threshold = len([i for i in sim if i > top_threshold])
    # index: [target_num]
    sim_index = sim_index[:min(top_k, top_k_threshold)]
    sim = [sim[i] for i in sim_index]
    print(sim_index)
    print(sim)
    return GetTopResItem(code=200, msg='Success', data=sim_index)


if __name__ == '__main__':
    uvicorn.run(app=app,
                host='0.0.0.0',
                port=args.port,
                workers=1)
