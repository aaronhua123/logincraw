import threading
import time

from logincraw import BaseCraw, session
app = BaseCraw(__name__)

@app.login
def gin():
    session.get('https://www.baidu.com')
    return session # 必须return session

# 带参数 gin = login()(gin)
# 不带参数 gin = login（gin）
@app.whether_login
def whether_login(session):
    r = session.get('https://www.baidu.com')
    if r is 'logined' or r.status_code==200:
        return False
    else:
        return False

@app.check_login(thread = 2)
def start_craw():
    for i in range(6):
        print('i am running',threading.currentThread().name)
        time.sleep(0.5)
    return 'crawling'

@app.check_login(thread = 1)
def main():
    for i in range(10):
        print('i am running start_craw_1',threading.currentThread().name)
        time.sleep(0.5)
    return 'start_craw_1'

if __name__ == '__main__':
    app.run()
    # or
    # start_craw()
