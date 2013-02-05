# encoding: utf-8
from django.http import HttpResponse
import pymongo

from django.utils.feedgenerator import Rss201rev2Feed
from django.contrib.syndication.views import Feed, FeedDoesNotExist
from django.shortcuts import get_object_or_404
from func import connectBlogDatabase

__author__ = 'Real'


from django.utils import feedgenerator
from datetime import datetime

def rss(request):

    host = request.get_host()
    db = connectBlogDatabase(request)
    info = db.infos.find_one()
    articles = db.articles.find(sort=[('PostOn', pymongo.DESCENDING)])

    feed = feedgenerator.Rss201rev2Feed(
        title = info['Title'],
        link = 'http://'+host,
        description = info['Subtitle'],
        language = 'zh-cn',
        feed_url = 'http://' + host + '/rss/',
    )

    for i in articles:
        feed.add_item(
            title = i['Title'],
            link = 'http://%s/article/%d/' % (host, i['Id']),
            pubdate = datetime.now(),
            description = i['Content']
        )

    return HttpResponse(feed.writeString('utf-8'),
        content_type='application/rss+xml; charset=utf-8')
