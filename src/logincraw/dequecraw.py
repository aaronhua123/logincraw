from collections import deque

class Deque(deque):
    def enter(self, ling,priority,func, argument):
        self.append(( func, argument))

    def run(self):
        func, args = self.pop()
        func(*args)

def go(a):
    print(f"nihao :{a}")
#
# ss = Deque()
# ss.enter(go,"asd")
# ss.run()
# ss.run()

import heapq
class PriorityQueue:
    def __init__(self):
        self._queue = []
        self._index = 0

    def enter(self,ling,priority,func,argument=()):
        heapq.heappush(self._queue,(-priority,self._index,(func,argument)))
        self._index +=1

    def run(self):
        func,arg = heapq.heappop(self._queue)[-1]
        return func(*arg)

if __name__ == '__main__':
    ss = PriorityQueue()
    ss.enter(0,1,go,("go",))
    ss.run()
