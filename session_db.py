# -*- coding: utf-8 -*-
# Created by go on 2019/4/1
# Copyright (c) 2019 go. All rights reserved.
# import json
import sqlite3
import os
from os import path

class SqLiteDB(object):
    def __init__(self):
        '''
        初始化cursor
        檢測session.db,是否存在表格session，没有则创建
        '''
        tablename = path.dirname(__file__)
        print(tablename)
        os.makedirs(tablename, exist_ok=True)
        self.db = tablename + '/session.db'
        # print('链接数据库')
        # print('操作成功')
        # self.checksession()
# 单例模式
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(SqLiteDB, "_instance"):
    #         if not hasattr(SqLiteDB, "_instance"):
    #             SqLiteDB._instance = object.__new__(cls)
    #     return SqLiteDB._instance

    def checksession(self):
        '''
        检测是否存在表session
        :return:
        '''
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            try:
                # cursor.execute('drop table session')
                cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='session'")
                # cursor.execute('insert into session (name,cookis) values (?, ?)',['asd','{cookie}'])
                # cursor.execute('select * from session')
                count = cursor.fetchone()
                print(count,'存在表session')
                if count[0] == 0:
                    cursor.execute('create table session (name varchar(30) PRIMARY KEY NOT NULL,cookies TEXT)')
                    print('创建session table')
                else:
                    print('已存在table')
            except Exception as e:
                print(e)
            finally:
                cursor.close()

    def querySession(self,name):
        '''
        查询session
        :param name: session 名称
        :return:
        '''
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(r"select * from session where name=?",(name,))
                one = cursor.fetchone()
                return one# ("name","json")
            except Exception as e:
                self.checksession()
                raise
            finally:
                cursor.close()


    def writeSession(self, name, cookies):
        '''
        写入session
        :param name: 对应的数据
        :param cookies: cookies的json数据
        :return:
        '''
        with sqlite3.connect(self.db) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('replace into session (name,cookies) values (?, ?)', (name, cookies))
                return cursor.rowcount
            except Exception as e:
                raise
            finally:
                cursor.close()


sessinoDb = SqLiteDB()

if __name__ == "__main__":
    db = SqLiteDB()
    # db.checksession()# 检测并创建表session
    import json
    # print(db.writeSession('ll',json.dumps("测试sessionDB",ensure_ascii=False)))
    print(json.loads(db.querySession('ll')[1]))


