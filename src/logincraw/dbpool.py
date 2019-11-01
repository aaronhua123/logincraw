# https://stackoverflow.com/questions/98687/what-is-the-best-solution-for-database-connection-pooling-in-python
# 本机数据库推荐不使用连接池，远程的数据库使用连接池。

import time
from abc import ABCMeta, abstractmethod
# import cx_Oracle as Oracle
import pymysql
from DBUtils.PooledDB import PooledDB
from logincraw.logs import logger


# conf = {
#     'user': 'root',
#     'password': 'Qt123456@',
#     'host': '192.168.1.102',
#     'port': 13306,
#     'db': 'education'
# }

# 帮助维护连接池的链接
class BaseConnect(object, metaclass=ABCMeta):
    _pool = None

    def __init__(self, **conf):
        self.conn = self._get_conn(conf)
        # self.cur = self.conn.cursor()

    @staticmethod
    @abstractmethod
    def _get_conn(conf):
        """
        一些 PoolDB 中可能会用到的参数，根据实际情况自己选择
        mincached：       启动时开启的空连接数量
        maxcached：       连接池最大可用连接数量
        maxshared：       连接池最大可共享连接数量
        maxconnections：  最大允许连接数量
        blocking：        达到最大数量时是否阻塞
        maxusage：        单个连接最大复用次数
        :param conf:        dict    连接Oracle的信息
        """
        pass

    def execute_sql(self, sql, args=None):
        """
        执行sql语句
        :param sql:     str     sql语句
        :param args:    list    sql语句参数列表
        """
        try:
            with self.conn.cursor() as cursor:
                if args:
                    cursor.execute(sql, args)
                else:
                    cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            logger.info(e, exc_info=True)
            raise

    def executemany(self, sql, args):
        """
        调用mysql的executemany方法，快速插入大量数据。
        :param sql:
        :param args:
        :return:
        """
        try:
            with self.conn.cursor() as cursor:
                result = cursor.executemany(sql, args)
            self.conn.commit()
            return result
        except Exception as e:
            logger.info(e, exc_info=True)
            raise

    def fetch_all(self, sql, args=None):
        """
        获取全部结果
        :param sql:     str     sql语句
        :param args:    list    sql语句参数
        :return:        tuple   fetch结果
        """
        try:
            with self.conn.cursor() as cursor:
                if args:
                    cursor.execute(sql, args)
                else:
                    cursor.execute(sql)
            self.conn.commit()
            return cursor.fetchall()
        except Exception as e:
            logger.info(e, exc_info=True)
            raise

    def __del__(self):
        """
        在实例资源被回收时，关闭该连接池
        """
        self.conn.close()
        # logger.info('del pool')


class MyConnect(BaseConnect):
    """
    mysql连接池，每实例化一次，获取一个连接。
    """
    @staticmethod
    def _get_conn(conf):
        logger.info('creating MyConnect')
        try:
            if MyConnect._pool is None:
                MyConnect._pool = PooledDB(pymysql, mincached=5, maxcached=30, **conf)  # 全局连接池
            return MyConnect._pool.connection()
        except Exception as e:
            logger.error(e)


class OracleConnect(BaseConnect):
    """ todo 未完成"""
    @staticmethod
    def _get_conn(conf):
        logger.info('creating OracleConnect')
        if OracleConnect._pool is None:
            OracleConnect._pool = PooledDB(Oracle, mincached=5, maxcached=30, **conf)
        return OracleConnect._pool.connection()


def MyConnect_demo():
    test_sql = "SELECT * FROM xinrui_get_app_list"
    my = MyConnect(**{
        'user': 'root',
        'password': 'Qt123456@',
        'host': '192.168.1.102',
        'port': 13306,
        'db': 'education'
    })
    res = my.fetch_all(test_sql)
    logger.info(res)


def OracleConnect_demo():
    test_sql = "show databases"

    my = OracleConnect(**{
        "dsn": "customer_service/Qt123456@@193.168.1.103:1522/ORCL",
    })
    res = my.execute_sql(test_sql)
    logger.info(res)


if __name__ == "__main__":
    pass

