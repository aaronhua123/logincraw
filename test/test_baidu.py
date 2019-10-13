from logincraw import BaseCraw,session
app = BaseCraw(__name__)

@app.main(thread = 5)
def main():
    r  = session.get('https://www.baidu.com')
    print(r.status_code)
    print(r.cookies)

if __name__ == '__main__':
    app.run()