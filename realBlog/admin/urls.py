# encoding: utf-8
import os

from django.conf.urls import patterns, include, url
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from realBlog.admin import article, category, link, other
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',

    url( r'^$', article.showAll),

    # Articles
    url( r'^edit-article/(\d+)/$', article.edit, {'hidden':False}),
    url( r'^delete-article/(\d+)/$', article.delete, {'hidden':False}),
    url( r'^new-article/$', article.new),

    # Categories
    url( r'^show-categories/$', category.showAll),
    url( r'^new-category/$', category.new),
    url( r'^edit-category/([0-9a-f]+)/$', category.edit),
    url( r'^delete-category/([0-9a-f]+)/$', category.delete),

    # Links
    url( r'^show-links/$', link.showAll),
    url( r'^new-link/$', link.new),
    url( r'^edit-link/([0-9a-f]+)/$', link.edit),
    url( r'^delete-link/([0-9a-f]+)/$', link.delete),

    # Hidden Articles
    url( r'^show-hidden-articles/$', article.showHiddens),
    url( r'^show-hidden-article/(\d+)/$', article.showHidden),
    url( r'^edit-hidden-article/(\d+)/$', article.edit, {'hidden':True}),
    url( r'^delete-hidden-article/(\d+)/$', article.delete, {'hidden':True}),

    # Settings
    url( r'^blog-settings/$', other.showSettings),
    url( r'^blog-plugins/$', other.showPlugins),

    url( r'^upload-xml/$', other.upload_xml),
    url( r'^import-and-output/$', other.import_and_output),
)


