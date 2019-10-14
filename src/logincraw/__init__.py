# 本项目的目的是提供一套方法去辅助登录的爬虫进行cookies的保持

# 目标爬虫的特性

# 1、需要长久的爬取，长期的保持登陆
# 2、需要做登陆验证的
# 3、可能有简单的验证码
# 4、对于登陆时敏感的，对登录次数有限制
# 5、提供兼容多线程的爬虫方式
# 6、session的本地化，极大的方便调试
from .app import BaseCraw,session
from .sched_app import Sched

