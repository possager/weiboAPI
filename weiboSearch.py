#_*_coding:utf-8_*_
import urllib2
from bs4 import BeautifulSoup
import pymongo
import html5lib
import dataEncode#因为只有登陆了才能访问全部的搜索链接

#数据库部分
client=pymongo.MongoClient('localhost',27017)
weibosearch=client['weibosearch']
weibosearchresult=weibosearch['weibosearchresult']


class searchpage:
    def __init__(self):
        self.searchurlmain='http://s.weibo.com/weibo/aaa?topnav=1&wvr=6&b=1'
        self.search_content=None
        self.result=None

    def _Init(self):
        loginer=dataEncode.sinaLogin(username='passager%40163.com', password='ll13715325265')
        loginer.initPara()
        loginer.enableCookie()  # 1
        loginer.getPreLoginJS()  # 2
        loginer.getPostData()
        #此函数执行完了之后也就自然登陆完了，后边的urllib2.urlopen方法自然都是用的这里变声明的cookie之类的东西。

    def searchfunc(self):
        self._Init()
        researchpage=urllib2.urlopen(self.searchurlmain)
        researchpageSoup=BeautifulSoup(researchpage,'html5lib')
        print researchpageSoup

if __name__ == '__main__':
    a=searchpage()
    a.searchfunc()