# encoding: utf-8
import urllib2
from django.http import HttpResponseRedirect
from func import get_current_blog
from realBlog.config.server import *

__author__ = 'Home'


class CheckIsAdminMiddleware(object):

    def process_view(self, request, view, args, kwargs):
        """newArticle, editArticle"""
        module = view.__module__
        if not module.find("realBlog.admin."):
            url = urllib2.quote(request.get_full_path()[1:])

            user = request.session.get('user')
            if user is None or not isAdmin(user, request):
                return HttpResponseRedirect('/login/?redirect='+url)

        return None

def isAdmin(user, request):
    blog = get_current_blog(request)
    if blog is not None:
        admins = blog[STR_ADMINS]
        if isinstance(admins, str) and admins == user['Username']:
            return True
        elif isinstance(admins, list) and user['Username'] in admins:
            return True

    return False


'''
    验证是否登录
'''
class CheckLoginMiddleware(object):

    def process_view(self, request, view, args, kwargs):
        """newArticle, editArticle"""
        module = view.__module__
        if not module.find("realBlog.admin."):
            url = urllib2.quote(request.get_full_path()[1:])

            user = request.session.get('user')
            if user is None:
                return HttpResponseRedirect('/login/?redirect='+url)

        return None




