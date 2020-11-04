# encoding: utf-8
"""
@version: 1.0
@author: Jarrett
@file: __init__
@time: 2020/11/4 15:10
"""
import datetime


class NowTime():
    """
    定义当前时间
    """

    def __init__(self):
        pass

    def now_time(self):
        curr_time = datetime.datetime.now()
        return datetime.datetime.strftime(curr_time, '%Y-%m-%d %H:%M:%S')
