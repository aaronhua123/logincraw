# logincraw
logincraw是一个简单易用的支持登陆保持的爬虫库。仅使用了requests,json,sqlite3数据库。

# 目的
在做一些系统的爬虫的时候，经常需要对登陆的session编写代码进行保持。所以把session保存的逻辑提取出来提供一套方法去辅助登录的爬虫进行cookies的保持。

# 目标爬虫的特性
1. 需要长久的爬取，长期的保持登陆
2. 需要做登陆验证的
3. 对于登陆时敏感的，对登录次数有限制
4. 提供兼容多线程的爬虫方式
5. session的本地化，极大的方便调试

对于无需登陆，或者登陆限制小的就不适用这个库。

# 安装
把库拖到工作目录中就可以使用。
例如：
```
/logincraw
/main.py
```

# 简单示例
```
from logincraw import BaseCraw, session
app = BaseCraw('baiducraw')

@app.login # 系统登陆逻辑，返回session
def login():
    session.get('https://www.baidu.com')
    return session # 必须 return session

@app.whether_login # 验证是否登陆成功的方法
def whether_login(session):
    r = session.get('https://www.baidu.com') # 请求系统的某个页面，用于检测是否登陆
    if r is 'logined':
        return True
    else:
        return False

@app.check_login(thread = 2) # 参数thread 启动的线程数。与app.run()搭配
def start_craw(): # 实际爬虫的逻辑
    print('i am running')
    return save_to_db()

if __name__ == '__main__':
    app.run() # 调用多线程方法
    # or
    # start_craw() # 调用本身的方法
```


