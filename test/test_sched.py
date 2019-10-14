# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:41
# @Author  : aaronhua

# 去管理app，web的方式配置采集参数？？？ 还是说在线下配？ 启动停止、定时启动。
from logincraw import schedapp
from test_baidu import app

config = {
    'hour': 20,
    'minute': 18,
    'second': 0,
    'microsecond': 0
}

schedapp(app.run,config)

