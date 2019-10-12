# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 16:07
# @Author  : aaronhua

import threading
import time
from logincraw import BaseCraw, session
app = BaseCraw(__name__)

@app.login
def login():
    session.get('https://www.baidu.com')
    return session # 必须return session

# 带参数 gin = login()(gin)
# 不带参数 gin = login（gin）
@app.whether_login
def whether_login(session):
    '''
    判断是否登录成功，已登录返回True，未登录返回False。
    :param session:全局的session
    :return:True or False
    '''
    r = session.get('https://www.baidu.com')
    return r is 'logined' or r.status_code==200

@app.protect()
def craw_a():
    for i in range(1):
        print('i am running craw_a',threading.currentThread().name)
        time.sleep(0.5)
    return 'crawling'

@app.protect()
def craw_b():
    for i in range(1):
        print('i am running craw_b',threading.currentThread().name)
        time.sleep(0.5)
    return 'crawling'

@app.main(thread = 3)
def main1():
    for i in range(1):
        craw_b()
        craw_a()
        craw_b()

@app.main(thread = 2)
def main2():
    for i in range(1):
        craw_a()
        craw_b()
        craw_a()

if __name__ == '__main__':
    # app.debug = True
    app.run() # 全局运行，所有checklogin就是
    # main.__wrapped__()
    # start_craw() # 检测login，登录测试