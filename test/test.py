# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 16:07
# @Author  : aaronhua
import random
from logincraw import BaseCraw, session
app = BaseCraw(__name__)
@app.login
def login():
    session.get('https://www.baidu.com')
    print('login')
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
    print('check')
    return random.choice([True,False])
    # return r is 'logined' or r.status_code==200

@app.protect
def craw_a():
    r = session.get('https://www.baidu.com')
    print('a',r.status_code)

@app.protect
def craw_b():
    r = session.get('https://www.baidu.com')
    print('b',r.status_code)

@app.main(thread = 3)
def main1():
    for i in range(10):
        craw_b()


@app.main(thread = 9)
def main2():
    for i in range(10):
        craw_a()

# 多线程模式是连续的多个分散的任务，分配到少量线程的
# 事件调度是任务的启动时间设定

if __name__ == '__main__':
    # app.debug = True
    # print(login())
    # app.run() # 全局运行，所有main就是
    # main.__wrapped__()
    # start_craw() # 检测login，登录测试
    # main1()
    # craw_a()
    print(__name__)
    print(__file__)