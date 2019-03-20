class Fib():
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        if self.a > 10000:
            raise StopIteration;
        return self.a

    def __getitem__(self, n):
        if isinstance(n, int):
            x, y = 0, 1
            for m in range(n):
                x, y = y, x + y
            return x
        # 并没有对step及负数等做处理,待改进
        if isinstance(n,slice):
            start = n.start
            stop = n.stop
            if start == None:
                start = 0
            if stop is None:
                raise IndexError
            a,b = 1,1
            L = []
            for m in range(stop):
                if m >= start:
                    L.append(a)
                    a,b = b,a+b
                else:
                    print('Wrong Slice')
            return L

    def __getattr__(self, item):
        if item == 'newAttr':
            return 'newAtter'
        raise AttributeError('\'Student\' object has no attribute \'%s\'' % item)

    def __call__(self, *args, **kwargs):
        print('Fib is callable')
        return self

if __name__ == '__main__':
    x = Fib()
    for n1 in x:
        print('first:%s' % n1)
    n2 = Fib()[1:20]
    print('second:%s' % n2)
    print('new attr: %s'%Fib().newAttr)
    # print('other attr: %s'%Fib().newAttr1)
    print(callable(max))
    print(callable(x))
    print(x())


