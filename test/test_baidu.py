import time
from concurrent.futures import ThreadPoolExecutor
from logincraw import BaseCraw,session
from logincraw.app import ss
app = BaseCraw(__name__)
from lxml import etree

exitcode = 1

@app.enter(3)
def main():
    r = session.get('http://www.baidu.com/s?wd=1&ie=UTF-8')
    # print(r.status_code)
    # print(r.cookies)
    r.encoding='utf-8'
    # print(r.text)
    tree = etree.HTML(r.content)
    href_list = tree.xpath('//div[@id="page"]/a/@href')
    # print(href_list)
    return base,0
    # s.enter(0, 2, base, argument=(0,))

def base(i):
    # 列表页1
    time.sleep(1)
    url = 'http://www.baidu.com/s?wd=1&pn={0}&oq=1&ie=utf-8&usm=2&rsv_pq=a20bbfea0043eae8&rsv_t=40eeF8O22GhFaaYqaAsG3Fqi8oNGkuzZffxHTvf4kQFDJ9P5qp0TYtaXvvg'.format(i)
    ss.enter(0,2,page,argument=(url,i))
    # page(url)
    time.sleep(10)
    print("dddddddddddd")
    # 阻塞 程序

def page(url,index):
    # 列表页二
    r = session.get(url)
    result = r.url
    print(result)
    for i in range(3):
        ss.enter(0,1,lml,argument=(f"{result}:done:{i}",))
    if index<50:
        base(index+10)
    else:
        global exitcode
        exitcode = 0

def lml(url):
    # 详情内容
    print(url)
    time.sleep(2)
    for i in range(3):
        ss.enter(0, 0, img, argument=(f"{url}:image:{i}",))

def img(img):
    print("==",img)
    time.sleep(2)

def go():
    global ss
    while True:
        ss.run(blocking=False)
        if exitcode==0 and ss.empty() is True:
            print('break')
            break

if __name__ == '__main__':
    start = time.time()
    with ThreadPoolExecutor() as executor:
        for i in range(5):
            executor.submit(go)
        main()
        print("main")
    # executor = ThreadPoolExecutor()
    # for i in range(10):
    #     executor.submit(go)
    # print("shutdown")
    # executor.shutdown()
    end = time.time()
    print(end-start)
