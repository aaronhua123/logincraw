import requests
from logincraw.lxml2 import Xpath

if __name__ == '__main__':
    r = requests.get('https://www.baidu.com',verify=False)
    x = Xpath(r.content)
    # print(x.xpath('//div'))
    print(x.path('//title/text()').first())
    # for i in x.xpath('//div'):
    #     print(i)
    #
    # for i in x.path('//div'):
    #     print(i)