from logincraw import BaseCraw,session
app = BaseCraw(__name__)

@app.main(thread=1)
def main():
    r  = session.get('https://www.baidu.com')
    print(r.status_code)
    print(r.cookies)

if __name__ == '__main__':
    config = {
        'day':'*',
        'hour': 15,
        'minute': 36,
        'second': 0,
        'microsecond': 0
    }
    app.sched(config)