# encoding: utf-8
import os
import re
import urllib
import urllib2
import hashlib

import pymongo

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt

from func import *

from datetime import datetime

__author__ = 'Home'



def index_user(request):

    db = connectAccountDatabase()
    info = db.infos.find_one()
    users = list(db.users.find())

    return render_admin_and_back(request, 'users.html', {
        'page':u'用户管理',
        'users':users,
        'selection':'users',
        })


@csrf_exempt
def register(request):
    '''
    注册账户
    '''
    if request.method == 'GET':
        setTemplateDir('admin')
        d = {}
        # 是否注册第一位管理员
        if request.GET.get('redirect') == 'install':
            # 取出第一位管理员
            blog = get_current_blog(request)
            admin = blog[STR_ADMINS]
            if isinstance(admin, list):
                admin = admin[0]

            d['admin'] = admin
            d['is_to_install'] = True # 标记注册后转到安装界面

        return render_to_response('register.html', d)

    elif request.method == 'POST':

        d = request.POST
        password = d['password']
        password_repeat = d['password-repeat']

        # 验证两次密码输入是否正确
        if password == password_repeat:

            db = connectAccountDatabase()

            # 检查用户是否已存在
            username = d['username']
            if db.users.find_one({'Username':username}):
                return redirect(request, '用户已存在', 'register/')

            # 检查Email是否已存在
            email = d['email']
            if db.users.find_one({'Email':email}):
                return redirect(request, 'Email已存在', 'register/')

            nickname = d['nickname']
            realname = d['realname']
            gender = d['gender']
            classname = d['classname']
            school = d['school']
            phone = d['phone']
            address = d['address']
            company = d['company']
            qq = d['qq']
            marry = d['marry']
            marrydate = d['marrydate']
            baby = d['baby']
            babyBirthDate = d['babyBirthDate']
            babyGender = d['babyGender']
            # 设置当前时间为注册时间
            regisDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # 对密码进行哈希
            hash = hashlib.sha1()
            hash.update((username+password).encode('utf8'))
            passwordHash = hash.hexdigest()

            # 插入用户信息
            db.users.insert({
                'Username': username,
                'Password':passwordHash,
                'Nickname':nickname,
                'Realname':realname,
                'Email':email,
                'Gender':gender,
                'Classname':classname,
                'School':school,
                'Phone':phone,
                'Address':address,
                'Company':company,
                'QQ':qq,
                'Marry':marry,
                'Marrydate':marrydate,
                'Baby':baby,
                'BabyBirthDate':babyBirthDate,
                'BabyGender':babyGender,
                'RegisDate':regisDate,
            })
            db.connection.disconnect()

            # 是否转到安装界面
            is_to_install = d['is-to-install'] == 'True'
            if is_to_install == False:
                user = db.users.find_one({'Username': username})
                request.session['user'] = user
                return redirect(request, '新建用户成功', 'admin/')
            
            return redirect(request, '新建用户成功', 'install/' if is_to_install else '')

        else:
            return redirect(request, '密码重复')
        
        
#### added by insKy -   
@csrf_exempt      
def reguser(request):
    '''
    注册新用户
    '''
    if request.method == 'GET':
        setTemplateDir('admin')
        d = {}
        # 是否注册第一位管理员
        if request.GET.get('redirect') == 'install':
            # 取出第一位管理员
            blog = get_current_blog(request)
            admin = blog[STR_ADMINS]
            if isinstance(admin, list):
                admin = admin[0]

            d['admin'] = admin
            d['is_to_install'] = True # 标记注册后转到安装界面

        return render_to_response('register_user.html', d)

    elif request.method == 'POST':

        d = request.POST
        password = d['password']
        password_repeat = d['password-repeat']

        # 验证两次密码输入是否正确
        if password == password_repeat:

            db = connectAccountDatabase()

            # 检查用户是否已存在
            username = d['username']
            if db.classmates.find_one({'Username':username}):
                return redirect(request, '用户已存在', 'register/')

            # 检查Email是否已存在
            email = d['email']
            if db.classmates.find_one({'Email':email}):
                return redirect(request, 'Email已存在', 'register/')

            realname = d['realname']

            # 对密码进行哈希
            hash = hashlib.sha1()
            hash.update((username+password).encode('utf8'))
            passwordHash = hash.hexdigest()

            # 插入用户信息
            db.classmates.insert({
                'Username': username,
                'Password':passwordHash,
                'Realname':realname,
                'Email':email,
                'Class':'c1', #默认都取c1
                'Date':'',
            })
            db.connection.disconnect()

            # 是否转到安装界面
            is_to_install = d['is-to-install'] == 'True'

#            return redirect(request, 'map_mark.html', 'install/' if is_to_install else '')
            return render_to_response('map_mark.html')
        else:
            return redirect(request, '密码重复')

def showHomepage(request, page):

    db = connectBlogDatabase(request)

    info = db.infos.find_one()
    page = int(page)
    count = db.articles.count()
#    per_page = info.get('ArticlesPerPage') or 10
    per_page = 10

    articles = list(
        db.articles.find(
        sort = [('PostOn', -1)],
        skip = (page-1)*per_page,
        limit = per_page
    ))

    info = db.infos.find_one()
    for a in articles:
        caculateLocalTimeInfo(info, a)

    categories = list(db.categories.find())
    links = list(db.links.find(sort=[('Order', pymongo.ASCENDING)]))

    return render_and_back(request, 'index.html', {
        'page':u'首页',
        'articles':articles,
        'links':links,
        'categories':categories,
        'paginator':{
            'Current': page,
            'Total': count / per_page + (1 if count%per_page else 0),
            'PerPage': per_page,
        },
    })

####  show blogs
def showBlogs(request, page):

    db = connectBlogDatabase(request)

    info = db.infos.find_one()
    page = int(page)
    count = db.articles.count()
#    per_page = info.get('ArticlesPerPage') or 10
    per_page = 10

    articles = list(
        db.articles.find(
        sort = [('PostOn', -1)],
        skip = (page-1)*per_page,
        limit = per_page
    ))

    info = db.infos.find_one()
    for a in articles:
        caculateLocalTimeInfo(info, a)

    categories = list(db.categories.find())
    links = list(db.links.find(sort=[('Order', pymongo.ASCENDING)]))

    return render_and_back(request, 'index.html', {
        'page':u'首页',
        'articles':articles,
        'links':links,
        'categories':categories,
        'paginator':{
            'Current': page,
            'Total': count / per_page + (1 if count%per_page else 0),
            'PerPage': per_page,
        },
    })

def showArticle(request, id):

    db = connectBlogDatabase(request)

    article = db.articles.find_one({'Id':int(id)})
    if article is None:
        return HttpResponse('404')

    info = db.infos.find_one()
    caculateLocalTimeInfo(info, article)

    categories = list(db.categories.find())
    links = list(db.links.find(sort=[('Order', pymongo.ASCENDING)]))

    return render_and_back(request, 'detail.html', {
        'page': u'文章 - ' + article['Title'],
        'article': article,
        'links': links,
        'categories':categories,
    })

def showCategory(request, category):

    db = connectBlogDatabase(request)

    category = urllib.unquote(category)
    categoryObject = db.categories.find_one({'Title': category})
    if categoryObject is None:
        return HttpResponse('404')

    links = db.links.find(sort=[('Order', pymongo.ASCENDING)])
    articles = db.articles.find({'Categories': category}, sort=[('PostOn', pymongo.DESCENDING)])
    categories = db.categories.find()

    return render_and_back(request, 'index.html', {
        'page': u'分类 - ' + category,
        'links':links,
        'articles':articles,
        'categories':categories,
        })

def showTag(request, tag):

    db = connectBlogDatabase(request)

    tag = urllib.unquote(tag)
    links = db.links.find(sort=[('Order', pymongo.ASCENDING)])
    articles = db.articles.find({'Tags': tag}, sort=[('PostOn', pymongo.DESCENDING)])
    categories = db.categories.find()

    return render_and_back(request, 'index.html', {
        'page': u'标签 - ' + tag,
        'links':links,
        'articles':articles,
        'categories':categories,
    })

@csrf_exempt
def install(request):

    blog = get_current_blog(request)
    if blog is None:
        return HttpResponse('安装前请配置server.py！')

    name = blog[STR_NAME]
    if not re.match(r'^\w+$', name):
        return HttpResponse(
            '博客名称"%s"不合法。规范的名称仅限字母、数字和下划线' % name
        )

    admin = blog[STR_ADMINS]
    if isinstance(admin, list):
        admin = admin[0]
    if not re.match(r'^\w+$', admin):
        return HttpResponse(
            '管理员名称"%s"不合法。规范的名称仅限字母、数字和下划线' % admin
        )

    # 检查博客是否已存在
    db = connectBlogDatabase(request)
    info = db.infos.find_one()
    if info is not None:
        return HttpResponse('博客已存在')

    # 检查第一个admin账户是否存在
    db = connectAccountDatabase()
    user = db.users.find_one({'Username':admin})
    if user is None:
        return redirect(request, '需要创建管理员账户', 'register/?redirect=install')

    if request.method == 'GET':

        admins = blog[STR_ADMINS]
        if isinstance(admin, list):
            admins = ', '.join(admins)

        setTemplateDir('admin')
        return render_to_response('install.html', {
            'host':request.get_host(),
            'name': blog[STR_NAME],
            'admins': admins,
        })

    elif request.method == 'POST':

        d = request.POST
        if d.get('is-blog-info-checked') is None:
            return redirect(request, '未勾选确认按钮', 'install/')

        db = connectBlogDatabase(request)
        db.categories.insert({
            'Title': '默认分类',
            'Description': '',
            'Order': 0
        })
        db.infos.insert({
            'TopId': 0,
            'Title': 'RealBlog',
            'Subtitle': 'A blog based of Django and MongoDB',
            'Description': 'No description',
            'Theme': 'default',
            'DefaultTimezone': 'Asia/Shanghai',
            'DefaultTimezoneOffset': '+8',
            'ArticlesPerPage' : 10,
            'CustomRss': '',
            'WeiboCode': '',
            'CommentCode': '',
            'LatestCommentsCode': '',
            'StatisticsCode': '',
            'StatisticsCodeInHead': False,
        })
        ensure_index_of_blog(db)

        db.connection.disconnect()

        return redirect(request, '安装完成', '')

@csrf_exempt
def login(request):
    # 普通访问
    if request.method == 'GET':
        return render_admin_and_back(request, 'login.html', {
            'page': '登录'
        })

    # 处理提交的表单
    elif request.method == 'POST':

        d = request.POST
        username = d['username']
        password = d['passwordHash']
        date = d['date']

        db = connectAccountDatabase()
        user = db.users.find_one({'Username': username})
        if user is None:
            return redirect(request, '用户名/密码错误', 'login/')

        hash = hashlib.sha1()
        hash.update(user['Password'])
        hash.update(date)

        if password != hash.hexdigest():
            return redirect(request, '用户名/密码错误', 'login/')

        request.session['user'] = user

        url = ''
        if 'redirect' in request.GET:
            url = urllib2.unquote(request.GET['redirect'])

#        return redirect(request, '登陆成功', url or 'admin/', 0)
#        return redirect(request, '登陆成功', 'admin/')
        
        # 上面的重定向方法只适合管理员real帐号，普通帐号总是重定向到登录界面，下面方法可以实现普通帐号登录
        db = connectBlogDatabase(request)
        info = db.infos.find_one()
        articles = list(db.articles.find(sort=[('PostOn', pymongo.DESCENDING)]))
        return render_admin_and_back(request, 'articles.html', {
            'page':u'文章',
            'articles':articles,
            'selection':'articles',
        })

def logout(request):

    if 'user' in request.session:
        del request.session['user']

    return redirect(request, '已退出', 'admin/', 0)


def getFile(request, ext):
    path = request.path
    abspath = os.path.abspath('.') + '/' + 'realBlog' + path
    if os.sep != '/':
        abspath = abspath.replace('/', '\\')

    stream = open(abspath, 'rb').read()

    mine = queryMineType(ext)

    return HttpResponse(stream, mimetype = mine)


#=======================================================================================================================
# maps function     by insKy
#=======================================================================================================================
def maps(request):
#    return HttpResponse(
#            'this is map page'
#        )
    setTemplateDir('admin')
    return render_to_response('map.html')

def showMarkers(request, type):
    #get makers from db
    
    db = connectMapsDatabase()
    if type == 'company':
        cmyLocation = list(db.companyaddress.find())
    elif type == 'home':
        cmyLocation = list(db.homeaddress.find())   
         
    jsonTxt = '['
#    116.41319275 39.96870074
    for it in cmyLocation:
        jsonTxt +='{lng:'+it['Lng']+',lat:'+it['Lat']+'},'
    
    jsonTxt+=']'
    
    
    res=HttpResponse()
    res['Access-Control-Allow-Origin']='*'
    res['Access-Control-Allow-Headers']='my-header,X-Requested-With'
#    res.write('[{lng:116,lat:39},{lng:116.1,lat:39.2},{lng:116.3,lat:39.3}]')
    res.write(jsonTxt)
    return res
#    return HttpResponse('[{lng:116,lat:39},{lng:116.1,lat:39.2},{lng:116.3,lat:39.3}]')

def navi(request):
        setTemplateDir('admin')
        return render_to_response('navi.html')
    
    
def naviMarkers(request):
    #get makers from db
    connection=pymongo.Connection('localhost',27017)
    db = connection.fornavi
    cmyLocation = list(db.lnglat.find().limit(10000))
         
    jsonTxt = '['
#    116.41319275 39.96870074
    for it in cmyLocation:
        jsonTxt +='{lng:'+it['Lng']+',lat:'+it['Lat']+'},'
    
    jsonTxt+=']'
    
    
    res=HttpResponse()
    res['Access-Control-Allow-Origin']='*'
    res['Access-Control-Allow-Headers']='my-header,X-Requested-With'
#    res.write('[{lng:116,lat:39},{lng:116.1,lat:39.2},{lng:116.3,lat:39.3}]')
    res.write(jsonTxt)
    return res


@csrf_exempt
def insertLocation(request, type):

    if request.method == 'GET':
        return render_admin_and_back(request, 'login.html', {
            'page': '登录'
        })

    # 处理提交的表单
    elif request.method == 'POST':

        d = request.POST
        cpyAddr = d['companyAddress']
        cpyLat = d['companyLat']
        cpyLng = d['companyLng']
#        date = d['date']


    db = connectMapsDatabase()
    
    if type == 'company':
        db.companyaddress.insert({
                'Address': cpyAddr,
                'Lat': cpyLat,
                'Lng': cpyLng
            })
    elif type == 'home':
        db.homeaddress.insert({
                'Address': cpyAddr,
                'Lat': cpyLat,
                'Lng': cpyLng
            })

    ensure_index_of_blog(db)

    db.connection.disconnect()

    return redirect(request, '111','maps/')

def queryMineType(ext):
    d = {
        'css': 'text/css',
        'js': 'application/x-javascript',
        'png': 'image/png',
        'jpg': 'image/jpeg',
        'gif': 'image/gif',
        'xml': 'text/xml',
        'swf': 'application/x-shockwave-flash',
        'html': 'text/html',
    }

    if ext in d:
        return d[ext]

    return ''
