from logincraw.dequecraw import Deque
from gevent import monkey;monkey.patch_all()
import gevent
import json
# import sched
import time
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
import logging as logger
import requests
from functools import wraps
# from logincraw.sched_app import schedapp
from .session_convert import SessionToList, ListToSession
from .session_db import sessinoDb

session = requests.Session()
ss = Deque()



class BaseCraw(ABC):
    def __init__(self, name):
        self.name = name
        self.route = {}
        self.priority = {}
        self.debug = False
        self.exitcode = 1

    def login(self, func):
        '''
        登录函数装饰器
        :param func:
        :return:
        '''
        self.dologin = func
        return func

    def whether_login(self, func):
        '''
        是否登录的装饰器，用于登录函数的加载
        :param func: 登录验证函数
        :return:
        '''
        self.whether_login_func = func
        return func

    def protect(self, func):
        '''
        检测装饰器，会获取线程的参数。进行session_controler的调用（先检测session）
        :param kwargs:
        :return:
        '''

        @wraps(func)
        def wrapper():
            return self.session_controler(func)

        return wrapper

    def session_controler(self, func):
        '''
        session 控制函数。debug模式下，查询数据库后，进行session检测和登录
        :param func:原函数
        :return:原函数的返回
        '''
        # @wraps(func)
        # def wrapper():
        if self.debug:
            # debug 模式，查询数据库进行登录
            db_data = sessinoDb.querySession(self.name)
            if db_data is None:
                self.dologin_and_save_session()
            else:
                _, json_list = db_data
                ListToSession(session, json.loads(json_list))
        # 正常运行模式，检测是否登录成功，然后执行函数
        if self.whether_login_func(session) is True:
            return func()
        else:
            self.dologin_and_save_session()
            return func()
        # return wrapper

    def dologin_and_save_session(self):
        '''
        执行登录并保存session
        :return:
        '''
        sess = self.dologin()
        session_list = SessionToList(sess)
        sessinoDb.writeSession(self.name, json.dumps(session_list))

    def run(self, debug=False):
        '''
        启动app，分配线程执行
        :param debug: debug为True则获取数据的session发起请求。通常用在测试的时候。
        :return: None
        '''
        if debug:
            self.debug = debug
        executor = ThreadPoolExecutor()
        for name, value in self.route.items():
            threadtime = value.get('thread')
            for i in range(threadtime):
                executor.submit(value['function'])

    def main(self, **kwargs):
        '''
        main装饰器，用于启动集体线程。有参数thread
        :param kwargs: thread （线程数）
        :return: None
        '''

        def wrapper(func):
            self.route[func.__name__] = kwargs
            # 原函数储存在 route 方法内
            self.route[func.__name__]['function'] = func  #
            # print(self.route)
            return func

        return wrapper




class ThreadCraw(object):
    def __init__(self, name: str):
        self.name: str = name
        self.priority: dict = {}
        self.exitcode: int = 1
        self.wrap = None

    def wait_and_check(self):
        for i in range(3):
            if ss.empty() is True:
                time.sleep(1)
            else:
                return False
        else:
            print('break')
            return True

    def go(self):
        print('go')
        global ss
        while True:
        #     try:
            try:
                time.sleep(1)
                ss.run()
            except Exception as e:
                # print(e)
                pass
        #         if self.exitcode == 0 and ss.empty() is True:
        #             if self.wait_and_check() is True:
        #                 break
        #     except BaseException as e:
        #         logger.error(e,exc_info=True)

    def run(self, thread: int = 1, max_workers=None):
        if not (isinstance(thread, int) and thread > 0): raise Exception(
            "thread must be int and greater than 0\n（线程数必须大于0且为int类型）")
        if self.wrap is None: raise Exception(
            "main function is None,place use app.main decorator\n（main函数为空，请在入口函数使用app.main装饰器）")
        # with ThreadPoolExecutor(max_workers=max_workers) as executor: # 阻塞主线程
        executor = ThreadPoolExecutor(max_workers=max_workers)
        _ = [executor.submit(self.go) for _ in range(thread)]  # .add_done_callback(self.executor_callback)
        print('self.wrap')
        # 主线程扔种子
        self.wrap()
        # executor.shutdown()

    def rung(self,thread=1):
        executor = ThreadPoolExecutor()
        executor.submit(self.wrap)
        r = [gevent.spawn(self.go) for _ in range(thread)]
        #print(r)
        gevent.joinall(r)


    @staticmethod
    def executor_callback(worker):
        # 捕捉线程错误
        logger.error("called worker callback function")
        worker_exception = worker.exception()
        # print(worker_exception)
        # raise worker_exception
        if worker_exception:
            logger.error(worker_exception,exc_info=True)

    def enter(self, func, *args):
        # print(dir(func.__class__.__class__))
        # print(func.__class__.__class__.__class__)
        if id(func) not in self.priority:
            raise Exception(f"function [{func.__name__}] not have priority. Place add app.setpriority decorator at [{func.__name__}]\n"
                            f"函数 [{func.__name__}] 没有设置权限值，请为函数 [{func.__name__}] 添加app.setpriority装饰器")
        ss.enter(0, self.priority[id(func)], func, argument=args)

    def setpriority(self, priority: int):
        def decorator(func):
            if not priority in range(1, 10): raise Exception(
                "setpriority must be int and between 1~9\n（setpriority的参数必须是int类型，范围在1~9）")
            self.priority[id(func)] = 10 - priority
            print(self.priority)
            return func

        return decorator

    def main(self, func):
        def wrapper(*args,**kwargs):
            return func(*args,**kwargs)
        self.wrap = wrapper
        return wrapper


