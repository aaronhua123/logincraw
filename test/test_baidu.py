import time
from logincraw import ThreadCraw
app = ThreadCraw(__name__)

@app.main
def main():
    # r = session.get('http://www.baidu.com/s?wd=1&ie=UTF-8')
    # # print(r.status_code)
    # # print(r.cookies)
    # r.encoding='utf-8'
    # # print(r.text)
    # tree = etree.HTML(r.content)
    # href_list = tree.xpath('//div[@id="page"]/a/@href')
    # print(href_list)

    # 推下一步任务
    app.enter(base,0)
    # s.enter(0, 2, base, argument=(0,))

@app.setpriority(1)
def base(i):
    # 列表页1
    time.sleep(1)
    url = 'http://www.baidu.com/s?wd=1&pn={0}&oq=1&ie=utf-8&usm=2&rsv_pq=a20bbfea0043eae8&rsv_t=40eeF8O22GhFaaYqaAsG3Fqi8oNGkuzZffxHTvf4kQFDJ9P5qp0TYtaXvvg'.format(i)
    # ss.enter(0,2,page,argument=(url,i))
    app.enter(page,url,i)
    # page(url)
    # time.sleep(10)
    # print("dddddddddddd")
    # 阻塞 程序

@app.setpriority(2)
def page(url,index):
    # 列表页二
    for i in range(10):
        time.sleep(1)
        # ss.enter(0,1,lml,argument=(f"{result}:done:{i}",))
        app.enter(lml,f"{url}:done:{i}")
    if index<10:
        base(index+1)
    else:
        app.exitcode=0

@app.setpriority(3)
def lml(url):
    # 详情内容
    print(url)
    time.sleep(1)
    for i in range(10):
        # ss.enter(0, 0, img, argument=(f"{url}:image:{i}",))
        app.enter(img,f"{url}:image:{i}")

@app.setpriority(4)
def img(img):
    print("==",img)
    time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    app.run(thread=100,max_workers=100)
    end = time.time()
    print(end-start)
