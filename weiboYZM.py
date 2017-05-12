import urllib2
import requests
import time
import random
import cookielib
import pymongo
from bs4 import BeautifulSoup


class weiboYZM:
    def __init__(self):

        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            }
        self.cookie=cookielib.LWPCookieJar()
        self.cookiehandler=urllib2.HTTPCookieProcessor(self.cookie)
        self.client=pymongo.MongoClient('localhost',27017)
        self.COL=self.client['WeiboLogin']
        self.DOC=self.COL['cookieDoc']


    def _Init(self):
        dict1=self.DOC.find_one({},{'_id':0,'ownner':0,'pwd':0})
        cookiestr=''
        for i in dict1:
            cookiestr+=(i+'='+dict1[i]+';')
        print cookiestr
        self.headers['cookie']=cookiestr
        print self.headers

    def run(self):
        self._Init()
        self.openner=urllib2.build_opener(self.cookiehandler)
        self.request=urllib2.Request(url='http://d.weibo.com/',headers=self.headers)

        response=self.openner.open(self.request)
        print response.url
        print response.read()



if __name__ == '__main__':
    a=weiboYZM()
    a.run()