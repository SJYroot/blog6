from django.shortcuts import render
from django.core.cache import cache

'''
def page_cache(view_func):
    def wrap(request):
        key = request.get_full_path()
        if cache.get(key) is not None:
            response = cache.get(key)
            print('缓存查询')
            return response
        response = view_func(request)
        cache.set(key,response)
        print('数据库查询')
        return response
    return wrap

'''
'''

def page_cache(view_func):
    def wrap(request, *args, **kwargs):
        key = 'PAGES-%s' % request.get_full_path()  # request是个对象，所以不能当，每次同一个进来都不一样  #request.path拿到的只是/foo/bar  所以用request.get_full_path()拿到的才是带参数的，才能唯一。
        # 从缓存获取响应 response
        response = cache.get(key)
        # 如果有 --- 直接返回
        if response is not None:
            return response
        else:
            # 如果没有 -- 直接执行下面的函数
            response = view_func(request, *args, **kwargs)
            # 将结果添加缓存
            cache.set(key, response)
            return response

    return wrap

'''


# 带参数的装饰器

def page_cache(timeout):
    def wrap1(view_func):
        def wrap2(request, *args, **kwargs):
            key = 'PAGES-%s' % request.get_full_path()  # request是个对象，所以不能当，每次同一个进来都不一样  #request.path拿到的只是/foo/bar  所以用request.get_full_path()拿到的才是带参数的，才能唯一。
            # 从缓存获取响应 response
            response = cache.get(key)
            # 如果有 --- 直接返回
            if response is not None:
                return response
            else:
                # 如果没有 -- 直接执行下面的函数
                response = view_func(request, *args, **kwargs)
                # 将结果添加缓存
                cache.set(key, response,timeout)
                return response
        return wrap2
    return wrap1














