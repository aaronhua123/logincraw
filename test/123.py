# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 11:16
# @Author  : aaronhua
import datetime
import sched,time
# 获取当前时间的函数， 时间等待的函数（可以使用一部的函数代替）
import threading

s = sched.scheduler(time.time, time.sleep)
import logging
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def print_time(a='default'):
    print("From print_time", time.time(), a)
    print(threading.currentThread().name)
    time.sleep(5)

def product():
    global s
    # print(time.time())
    # a =s.enterabs(time.time()+10,3,print_time,argument=('enterabs',))
    # #s.enter(10, 1, print_time)
    # s.enter(5, 2, print_time, argument=('enter',))
    # #s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
    # print(s.queue)
    # s.cancel(a)
    while True:
        s.enter(0, 2, print_time, argument=('enter',)) # 阻塞5秒钟，后运行
        # s.enterabs(time.time()+5,2,print_time,argument=('enterabs+5',))
        # s.enterabs(time.time()+5,2,print_time,argument=('enterabs+10',))
        time.sleep(1)


def dull():
    global s
    while True:
        next_ev = s.run(False) # 非阻塞
        if next_ev is not None:
            time.sleep(min(2, next_ev))
        else:
            #print(next_ev)
            time.sleep(2)
def queue():
    global s
    while True:
        print(len(s.queue))
        time.sleep(1)
    #s.run()
# a = datetime.datetime.now()
# print(dir(a))
# b = a.replace(hour=12,minute=15,second=0,microsecond=0)
# print(b)
# print(b.timestamp())
# print(time.time())
# print_time()
# from concurrent.futures import ThreadPoolExecutor
# exe = ThreadPoolExecutor()
# exe.submit(product)
# exe.submit(dull)
# exe.submit(dull)
# f = exe.submit(queue)
def go():
    s.enter(0, {}[id(1)], queue)

if __name__ == '__main__':
    # from concurrent.futures import ThreadPoolExecutor
    # exe = ThreadPoolExecutor()
    # exe.submit(go)
    assert id(1) in {},"error"
