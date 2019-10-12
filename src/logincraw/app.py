import json
from abc import ABC
from concurrent.futures import ThreadPoolExecutor
import requests

from .session_convert import SessionToList, ListToSession
from .session_db import sessinoDb
session = requests.Session()

class BaseCraw(ABC):

    def __init__(self, name):
        self.name = name
        self.route = {}

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

    def check_login(self, **kwargs):
        def wrapper(func):
            self.route[func.__name__] = kwargs
            self.route[func.__name__]['function'] = func
            print(self.route)
            return self.session_controler(func)
        return wrapper

    def run(self):
        executor = ThreadPoolExecutor(max_workers=4)
        for name, value in self.route.items():
            threadtime = value.get('thread')
            for i in range(threadtime):
                executor.submit(value['function'])

    def session_controler(self,func):
        db_data = sessinoDb.querySession(self.name)
        if db_data is None:
            self.dologin_and_save_session()
        else:
            _, json_list = db_data
            ListToSession(session, json.loads(json_list))# 提取session的json数据

        if self.whether_login_func(session) is True:
            return func()
        else:
            raise Exception("relogin error")

    def dologin_and_save_session(self):
        sess = self.dologin()
        session_list = SessionToList(sess)
        sessinoDb.writeSession(self.name,json.dumps(session_list))


