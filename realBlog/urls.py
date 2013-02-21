# encoding: utf-8
from django.conf.urls import patterns, include, url
from rss import rss
import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'realBlog.views.home', name='home'),
    # url(r'^realBlog/', include('realBlog.foo.urls')),

    # 首页
#    url( r'^$', views.showHomepage, {'page': 1}),
    url( r'^$', views.maps),
    url( r'^blog/$', views.showHomepage, {'page': 1}),
    url( r'^page/(\d+?)/$', views.showHomepage),

    # 调试时取得静态文件
    url( r'\.(css|js|png|jpg|gif|xml|swf|html)$', views.getFile),

    url( r'^login/', views.login),
    url( r'^logout/', views.logout),
    url( r'^register/$', views.register),
    ## added by insKy - register new user
    url( r'^reguser/$', views.reguser),
    url( r'^install/$', views.install),
    url( r'^article/(\d+?)/$', views.showArticle),
    url( r'^category/(.+?)/$', views.showCategory),
    url( r'^tag/(.+?)/$', views.showTag),

    # RSS
    url( r'^rss/$', rss),

    # Admin
    url( r'^admin/', include('realBlog.admin.urls')),

    
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    
    #===================================================================================================================
    # maps by insKy
    #===================================================================================================================
#         北三环东路辅路  39.96975322&mistakeInfoLng=116.43722534
    url(r'^maps/$', views.maps),
    url(r'^maps/getmarkers/(.+?)/$', views.showMarkers),
    url(r'^maps/submit/(.+?)/$', views.insertLocation),
    
    url(r'^navi/$', views.navi),
    url(r'^getnavimarkers/$', views.naviMarkers)
)
