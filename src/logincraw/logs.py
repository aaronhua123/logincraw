# todo 库的日志模块，提供框架日志和用户日志
import logging
import logging.config
import os

# 读取默认配置的路径
from functools import wraps

os.makedirs('logs',exist_ok=True)
curpath=os.path.dirname(os.path.realpath(__file__))
cfgpath=os.path.join(curpath,"logging.conf")

# 通过配置获取logger（fileLogger）
# level等级可以手动设置
logging.config.fileConfig(cfgpath)
# logger = logging.getLogger("fileLogger")
logger = logging.getLogger("rotatingfileLogger")
logging = logging

def log(func):
    """
    log装饰器，包裹错误，打印日志
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args,**kwargs)
        except Exception as e:
            logger.error(e,exc_info=True)
    return wrapper

if __name__ == '__main__':
    while 1:
        logger.info("check")