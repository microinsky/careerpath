# encoding: utf8
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from realBlog.admin.timezone import getTimezoneObject
from realBlog.func import get_upload_path, getThemes, connectBlogDatabase, render_admin_and_back, redirect
from realBlog.config.server import BLOGS

__author__ = '在何方'

@csrf_exempt
def showSettings(request):

    db = connectBlogDatabase(request)
    info = db.infos.find_one()

    if request.method == 'GET':#'POST'
        return render_admin_and_back(request, 'blog-settings.html', {
            'page': u'管理 - 设置',
            'theme': info.get('Theme'),
            'themes': getThemes(),
            'subtitle': info.get('Subtitle'),
            'description': info.get('Description'),
            'customRss': info.get('CustomRss'),
            'articlesPerPage': info.get('ArticlesPerPage'),
            'defaultTimezone': info.get('DefaultTimezone'),
            'defaultTimezoneOffset': info.get('DefaultTimezoneOffset'),
            'selection': 'blog-settings',
            })

    elif request.method == 'POST':

        d = request.POST

        update = {
            'Theme': d['blog-theme'],
            'Title': d['blog-title'],
            'Subtitle': d['blog-subtitle'],
            'Description': d['blog-description'],
            'CustomRss': d['blog-customRss'],
            'ArticlesPerPage': int(d['blog-articles-per-page']),
            'DefaultTimezone': d['blog-default-timezone'],
            'DefaultTimezoneOffset': d['blog-default-timezone-offset'],
        }

        # 时区和其与UTC的偏差
        timezone = d['blog-default-timezone']
        offset = d['blog-default-timezone-offset']
        if getTimezoneObject(timezone, offset):
            update['Timezone'] = timezone
            update['TimezoneOffset'] = offset

        db.infos.update(info, {'$set':update})

        return redirect(request, '设置保存成功', 'admin/')

@csrf_exempt
def showPlugins(request):

    db = connectBlogDatabase(request)
    info = db.infos.find_one()

    if request.method == 'GET':#'POST'
        return render_admin_and_back(request, 'blog-plugins.html', {
            'page': u'管理 - 插件',
            'weiboCode': info.get('WeiboCode'),
            'commentCode': info.get('CommentCode'),
            'latestCommentsCode': info.get('LatestCommentsCode'),
            'statisticsCode': info.get('StatisticsCode'),
            'statisticsCodeInHead': info.get('StatisticsCodeInHead'),
            'selection': 'blog-plugins',
            })

    elif request.method == 'POST':

        d = request.POST
        update = {
            'WeiboCode': d['weibo-code'],
            'CommentCode': d['blog-comment-code'],
            'LatestCommentsCode': d['blog-latest-comments-code'],
            'StatisticsCode': d['blog-statistics-code'],
            'StatisticsCodeInHead': d.get('blog-statistics-code-in-head')==u'on',
        }

        db.infos.update(info, {'$set':update})

        return redirect(request, '插件保存成功', 'admin/')

@csrf_exempt
def upload_xml(request):
    try:
        file = request.FILES['data']
        file_save = get_upload_path(file.name)
        print file_save
        save = open(get_upload_path(file.name), 'wb')
        for chunk in file.chunks():
            save.write(chunk)
        save.close()
        return HttpResponse('1', 'text/plain')
    except Exception, e:
        return HttpResponse('failed:'+e.message, 'text/plain')


def import_and_output(request):
    return render_admin_and_back(request, 'import-and-output.html', {'selection': 'import-and-output',})