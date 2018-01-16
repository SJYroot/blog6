# coding: utf-8
from django import db
from django.shortcuts import render, redirect
from math import ceil

from post.models import Article, Comment
from post.helper import page_cache

from django.core.cache import cache
# settings里设置，直接就认为已经配置好了。 使用的时候 pip install django_redis
# from redis import Redis   # redis自己的接口，更底层一些。现在直接用上述的cache接口就行
# cache.set('xxx',article)   # 因为多个文章，所以键设成aid就能区分。
# cache.get('xxx')  # 类型不会变化，存什么取什么

# 但是用redis
# r = Redis()
# r.set
# r.get(123)  # 拿到的是bytes，需要dumps和loads的封装

# 综上，用cache就行

'''
def home(request):
    articles = Article.objects.all()
    return render(request, 'home.html', {'articles': articles})
'''

@page_cache(10)
def home(request):
    # 计算总页数
    count = Article.objects.count()
    pages = ceil(count/5)  # 一页五个，分多少页  向上取整

    # 获取当前页数
    page = int(request.GET.get('page',1))  # 默认是1
    page = 0 if page < 1 or page >= (pages+1) else (page-1)  # 普通人1开始，程序员0开始

    # 取出当前页面的文章
    start = page * 5
    end = start + 5

    articles = Article.objects.all()[start:end]
    return render(request, 'home.html',
                  {'articles': articles,'page':page,'pages':range(pages)})

'''
# 一
def article(request):
    aid = int(request.GET.get('aid', 1))
    aidd = str(aid)+'sjy'
    if cache.get(aidd) :
        article,comments =  cache.get(aidd)[0], cache.get(aidd)[1]
        print('缓存查询')
        return render(request, 'article.html', {'article': article, 'comments': comments})

    article = Article.objects.get(id=aid)
    comments = Comment.objects.filter(aid=aid)
    cache.set(aidd, [article,comments])
    print('数据库查询')
    return render(request, 'article.html', {'article': article, 'comments': comments})
'''
'''
# 二
# comments经常变化，所以不用缓存
def article(request):
    aid = int(request.GET.get('aid', 1))
    key = 'article-%s'%aid
    article = cache.get(key)
    print('Cache get is:%s'%article)

    if article is None:
        print('Get from DB')
        article = Article.objects.get(id=aid)
        cache.set(key,article)

    comments = Comment.objects.filter(aid=aid)
    return render(request, 'article.html', {'article': article, 'comments': comments})

'''

# 缓存更新？

# 用装饰器，不改变源代码
@page_cache(30)
def article(request):
    aid = int(request.GET.get('aid', 1))
    article = Article.objects.get(id=aid)
    comments = Comment.objects.filter(aid=aid)
    return render(request, 'article.html', {'article': article, 'comments': comments})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        article = Article.objects.create(title=title, content=content)
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        return render(request, 'create.html')


def editor(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        article = Article.objects.get(id=aid)
        article.title = title
        article.content = content
        article.save()
        return redirect('/post/article/?aid=%s' % article.id)
    else:
        aid = int(request.GET.get('aid', 0))
        article = Article.objects.get(id=aid)
        return render(request, 'editor.html', {'article': article})


def comment(request):
    if request.method == 'POST':
        # form = CommentForm(request.POST)
        name = request.POST.get('name')
        content = request.POST.get('content')
        aid = int(request.POST.get('aid'))

        Comment.objects.create(name=name, content=content, aid=aid)
        return redirect('/post/article/?aid=%s' % aid)
    return redirect('/post/home/')


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')

        articles = Article.objects.filter(content__contains=keyword)
        return render(request, 'home.html', {'articles': articles})
