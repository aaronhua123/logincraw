import json
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
import requests
from functools import wraps
from .session_convert import SessionToList, ListToSession
from .session_db import sessinoDb
session = requests.Session()

class BaseCraw(ABC):

    def __init__(self, name):
        self.name = name
        self.route = {}
        self.debug = False

    def login(self,func):
        self.dologin = func
        def wrapper():
            return func
        return wrapper

    def whether_login(self,func):
        self.whether_login_func = func
        def wrapper():
            return func
        return wrapper

    def protect(self,**kwargs):
        '''
        检测装饰器，会获取线程的参数。进行session_controler的调用（先检测session）
        :param kwargs:
        :return:
        '''
        def wrapper(func):
            return self.session_controler(func)
        return wrapper

    def run(self,debug=False):
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

    def dologin_and_save_session(self):
        '''
        执行登录并保存session
        :return:
        '''
        sess = self.dologin()
        session_list = SessionToList(sess)
        sessinoDb.writeSession(self.name,json.dumps(session_list))

    def session_controler(self,func):
        @wraps(func)
        def wrapper():
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
        return wrapper

    def main(self,**kwargs):
        def wrapper(func):
            self.route[func.__name__] = kwargs
            self.route[func.__name__]['function'] = func
            print(self.route)
        return wrapper
