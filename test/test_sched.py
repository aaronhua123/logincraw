# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:41
# @Author  : aaronhua

# 去管理app，web的方式配置采集参数？？？ 还是说在线下配？ 启动停止、定时启动。
from logincraw import Sched

sch = Sched()
config = {
    'day': '*',
    'hour': 14,
    'minute': 33,
    'second': 0,
    'microsecond': 0
}

def run():
    print("i run")

run()
