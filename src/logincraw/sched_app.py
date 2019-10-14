# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 14:09
# @Author  : aaronhua
import datetime
import sched,time
def schedapp(func,config):
    s = sched.scheduler(time.time, time.sleep)
    now = datetime.datetime.now()
    taskdate = now.replace(**config)
    s.enterabs(taskdate.timestamp(), 0, func)
    s.run()


class Sched:
    s = sched.scheduler(time.time, time.sleep)
    # def __init__(self):
    #     self.config = config
    def sched(self,config):
        def wrapper(func):
            def wrap():
                while True:
                    # now = datetime.datetime.now()
                    # taskdate = now.replace(**config)
                    # self.s.enterabs(taskdate.timestamp(), 0, func)
                    self.s.enter(5,0, func)
                    self.s.run()
            return wrap
        return wrapper


if __name__ == '__main__':

    s = sched.scheduler(time.time, time.sleep)

    func = lambda x:print(x)
    config = {
        'hour': 14,
        'minute': 33,
        'second': 0,
        'microsecond': 0
    }
    check = False
    # 阻塞循环模式
    while True:
        now = datetime.datetime.now()
        if check:
            taskdate = now.replace(day=now.day+1,**config)
        else:
            taskdate = now.replace(**config)
            check = True
        print(taskdate)
        s.enterabs(taskdate.timestamp(), 0, func, argument=('enter',))  # 阻塞5秒钟，后运行
        print(s.queue)
        s.run()