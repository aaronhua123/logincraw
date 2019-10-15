# -*- coding: utf-8 -*-
# @Time    : 2019/10/14 12:26
# @Author  : aaronhua

from flask import Flask

app= Flask(__name__)

@app.route('/')
def index():
    return 'hello'

if __name__ == '__main__':
    app.run()