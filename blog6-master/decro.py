from time import time
def timer(times):
    def wrap1(func):
        def wrap2(*args,**kwargs):
# 这里不写x，y因为如果后面装别的，变了呢。装饰器是可以给任意一个函数用的。
            timen = time()
            s = 0
            for i in range(times):
                 s = func(*args, **kwargs)
            timeadd = time()-timen
            return s,timeadd
        return wrap2
    return wrap1

@timer(100000)
def foo(x,y):
    return x**y

print(foo(9,3))