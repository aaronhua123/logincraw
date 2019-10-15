import time
from logincraw import ThreadCraw

app = ThreadCraw(__name__)


@app.main  # 主线程扔种子函数
def main():
    '''
    添加种子，不需要设置权限。
    :return:
    '''
    for i in range(10):
        time.sleep(1)
        print(f"main {i}")
        app.enter(page, f"main {i}")
    app.exitcode = 0


@app.setpriority(1)
def page(a):
    # raise
    for i in range(10):
        time.sleep(1)
        print(a + f":page {i}")
        app.enter(img, a + f":page {i}")


@app.setpriority(2)
def img(b):
    for i in range(10):
        time.sleep(1)
        print(b + f":img {i}")
        app.enter(end, b + f":img {i}")


@app.setpriority(3)
def end(c):
    time.sleep(1)
    print(c + ":end")


if __name__ == '__main__':
    # app.run(thread=100,max_workers=100)
    app.rung(100)