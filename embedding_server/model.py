#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：fd_backend_alarm_match 
@File    ：model.py
@IDE     ：PyCharm 
@Author  ：Logan
@Date    ：2023/11/29 下午4:15 
"""

from pydantic import BaseModel
from typing import Union, List


class GetTopReqItem(BaseModel):
    """
    """
    source: List[str]
    target: List[str]
    top_k: int = 5
    top_threshold: float = 0.75


class GetTopResItem(BaseModel):
    code: int
    msg: str
    data: List
