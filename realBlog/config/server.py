# encoding: utf-8

DEBUG = True

DATABASE_HOST = '127.0.0.1'
DATABASE_PORT = 27017
DATABASE_USERNAME = None
DATABASE_PASSWORD = None

STR_NAME = 'Name'
STR_ADMINS = 'Administrators'

BLOGS = {
    '127.0.0.1:8082':{
        STR_NAME: 'realBlog',  #it should be changed when developing..
        STR_ADMINS: 'real',
    }
}