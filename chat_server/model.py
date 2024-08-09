#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：chat_server 
@File    ：model.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/12/7 上午9:25 
"""

from pydantic import BaseModel


class ChatReqItem(BaseModel):
    inputs: str
    history: list


class ChatResItem(BaseModel):
    code: int
    msg: str
    data: str
