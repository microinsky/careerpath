# encoding: utf-8
import pymongo
import pytz

from datetime import datetime, timedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from realBlog.admin.timezone import getTimezoneObject, isDaylightSavingTime
from realBlog.func import *

@csrf_exempt
def new(request):

    db = connectBlogDatabase(request)

    # 普通访问
    if request.method == 'GET':
        info = db.infos.find_one()
        return render_admin_and_back(request, 'edit-article.html', {
            'page':u'新文章',
            'categories': db.categories.find(),
            'article':{
                'Timezone': info.get('DefaultTimezone'),
                'TimezoneOffset': info.get('DefaultTimezoneOffset'),
                'UseDefaultTimezone': info.get('Timezone') is None,
                },
            })

    elif request.method == 'POST':

        d = request.POST

        # 取得Article内容
        a, res = getArticleContent(d)
        if res is not None:
            return HttpResponse('标题与正文都不能为空')

        # Author
        user = request.session.get('user')
        a['Author'] = {
            'Username':user['Username'],
            'Nickname':user['Nickname'],
            'Email':user['Email'],
        }

        # 是否存放在隐藏文章集合
        hidden_now = d.get('hidden')=='on'
        articles = db.hidden_articles if hidden_now else db.articles

        # Id
        info = db.infos.find_one()
        a['Id'] = info['TopId']
        articles.insert(a)

        # 更新TopId值
        db.infos.update(info, {"$set":{'TopId': info['TopId']+1}})

        return HttpResponse('/admin/')

@csrf_exempt
def edit(request, id, hidden=False):

    id = int(id)
    db = connectBlogDatabase(request)

    # 普通访问
    if request.method == 'GET':
        # 区别隐藏日志和普通日志
        articles = db.hidden_articles if hidden else db.articles
        a = articles.find_one({'Id': id})
        if a is None:
            return HttpResponse('404')

        categories = list(db.categories.find())
        for c in categories:
            c['Checked'] = c['Title'] in a['Categories']

        cats = ','.join(a['Categories'])
        tags = ','.join(a['Tags'])

        info = db.infos.find_one()
        a['UseDefaultTimezone'] = a.get('Timezone') is None
        a['Timezone'] = a.get('Timezone') or info.get('Timezone')
        a['TimezoneOffset'] = a.get('TimezoneOffset') or info.get('TimezoneOffset')

        return render_admin_and_back(request, 'edit-article.html', {
            'page':u'编辑文章',
            'categories': categories,
            'cats': cats,
            'tags': tags,
            'article': a,
            'hidden': hidden,
        })

    elif request.method == 'POST':

        d = request.POST

        # 旧的Article
        src = db.hidden_articles if hidden else db.articles
        old = src.find_one({'Id': id})

        # 新的Article
        a, res = getArticleContent(d, old['PostOn'])
        if res is not None:
            return HttpResponse(res)

        hidden_now = request.POST.get('hidden')=='on'

        if hidden == hidden_now:
            src.update({'Id': id}, {'$set':a})

        else:
            a['Id'] = old['Id']
            a['Author'] = old['Author']
            dst = db.hidden_articles if hidden_now else db.articles
            dst.insert(a)
            src.remove(old)

        return HttpResponse('Ok')

def delete(request, id, hidden=False):

    db = connectBlogDatabase(request)
    id = int(id)

    src = db.hidden_articles if hidden else db.articles

    if request.method == 'GET':
        article = src.find_one({'Id': id})
        if article is None:
            return HttpResponse(404)

        src.remove({'Id': id})

        return redirect(request, '删除成功，即将返回前一页...', 'admin/')

def showAll(request):

    db = connectBlogDatabase(request)
    info = db.infos.find_one()
    articles = list(db.articles.find(sort=[('PostOn', pymongo.DESCENDING)]))

    for a in articles:
        caculateLocalTime(info, a)

    return render_admin_and_back(request, 'articles.html', {
        'page':u'文章',
        'articles':articles,
        'selection':'articles',
        })

def showHidden(request, id):

    db = connectBlogDatabase(request)

    article = db.hidden_articles.find_one({'Id':int(id)})
    if article is None:
        return HttpResponse(404)

    return render_admin_and_back(request, 'show-hidden-article.html', {
        'page':u'隐私文章 - '+ article['Title'],
        'article':article,
        })

def showHiddens(request):

    db = connectBlogDatabase(request)
    info = db.infos.find_one()
    articles = list(db.hidden_articles.find(sort=[('PostOn', pymongo.DESCENDING)]))
    for a in articles:
        caculateLocalTime(info, a)

    return render_admin_and_back(request, 'show-hidden-articles.html', {
        'page':u'隐私文章',
        'articles':articles,
        'selection':'hidden-articles',
    })

def getArticleContent(d, postOn = None):
    '''
    取得表单中文章的内容
    '''
    if d['title'] is None or d['content'] is None:
        return None, '标题与正文都不能为空'

    a = {
        'Title':d['title'],
        'Content':d['content'],
    }

    def split_and_strip(s):
        return [i.strip() for i in s.split(',') if i!='' ]

    a['Categories'] = split_and_strip(d['categories'])
    a['Tags'] = split_and_strip(d['tags'])

    postOn = (postOn or datetime.utcnow())
    a['PostOn'] = postOn

    # 时区相关
    if d['use-default-timezone'] == 'false':
        timezone = d.get('timezone')
        offset = d.get('timezone-offset')

        # 验证时区是否有效
        tz = getTimezoneObject(timezone, offset)
        if tz is not None:
            a['Timezone'] = timezone
            a['TimezoneOffset'] = offset
            a['IsDst'] = isDaylightSavingTime(tz, postOn)
        else:
            return None, '无效的时区'
    else:
        a['Timezone'] = None
        a['TimezoneOffset'] = None
        a['IsDst'] = None

    return a, None
