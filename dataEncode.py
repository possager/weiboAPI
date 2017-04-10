import urllib2
import cookielib
from bs4 import BeautifulSoup
import html5lib
import base64
import re
import rsa
import json
import requests
import urllib
import binascii


class sinaLogin:

    def __init__(self,username=None,password=None):
        self.username=username
        self.password=password
        self.header=None
        self.cookie=None


    def initPara(self):
        self.header={
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
        }
        return self


    def getPreLoginJS(self):
        url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        response=urllib2.urlopen(url).read()
        data1=re.findall(r'\((\{.*?\})\)',response)[0]
        datajson=json.loads(data1)
        self.rsakv=datajson['rsakv']
        self.nonce=datajson['nonce']
        self.pubkey=datajson['pubkey']
        self.servertime=datajson['servertime']

        return self


    def enableCookie(self,IPproxy=False):
        self.cookie=cookielib.LWPCookieJar()
        self.cookieHandler=urllib2.HTTPCookieProcessor(self.cookie)
        if IPproxy:
            proxy_support=urllib2.ProxyHandler({'http':'http://115.85.233.94:80'})
            openner=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler,proxy_support)
        else:
            openner=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler)
        urllib2.install_opener(openner)
        urllib2.install_opener(openner)

        return self


    def getPostData(self):

        self.username=base64.encodestring(self.username)
        rsapubkey=int(self.pubkey,16)
        RSAKey=rsa.PublicKey(rsapubkey,65537)
        codestr=str(self.servertime)+'\t'+str(self.nonce)+'\n'+str(self.password)
        pwd=rsa.encrypt(codestr,RSAKey)
        self.password=binascii.b2a_hex(pwd)
        self.postdata={
            'cdult':'3',
            'domain':'sina.com.cn',
            'encoding':'UTF-8',
            'entry':'account',
            'from': 'null',
            'gateway': '1',
            'nonce': self.nonce,
            'pagerefer':'http://login.sina.com.cn/crossdomain2.php?action=login&r=http%3A%2F%2Flogin.sina.com.cn%2F',
            'prelt': '98',
            'pwencode': 'rsa2',
            'returntype': 'TEXT',
            'rsakv': self.rsakv,
            'savestate': '30',
            'servertime':self.servertime,
            'service': 'account',
            'sp':self.password,
            'sr': '1920 * 1080',
            'su': self.username.replace('\n',''),
            'useticket': '0',
            'vsnf': '1'
        }
        return self


    def login(self):
        loginURL='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
        request1=urllib2.Request(headers=self.header,url=loginURL,data=urllib.urlencode(self.postdata))

        responseLogin=urllib2.urlopen(request1).read()
        responseLoginJson=json.loads(responseLogin)
        # print responseLogin
        if responseLoginJson['retcode']=='0':
            print responseLoginJson['retcode']
            crossDomainUrlList=responseLoginJson['crossDomainUrlList']
            # print crossDomainUrlList

            self._webread(crossDomainUrlList[0])
            self._webread(crossDomainUrlList[1])
            self._webread(crossDomainUrlList[2])
            self._webread('http://login.sina.com.cn/crossdomain2.php?action=login')
            self._webread('http://i.sso.sina.com.cn/js/ssologin.js')
            self._webread('https://login.sina.com.cn/')
            # print self._webread('http://my.sina.com.cn')

            # a=urllib2.urlopen(crossDomainUrlList[0]).read()
            # b=urllib2.urlopen(crossDomainUrlList[1]).read()
            # c=urllib2.urlopen(crossDomainUrlList[2]).read()
            # d=urllib2.urlopen('http://login.sina.com.cn/crossdomain2.php?action=login')
            # e=urllib2.urlopen('http://i.sso.sina.com.cn/js/ssologin.js')
            # f=urllib2.urlopen('https://login.sina.com.cn/')
            # g=urllib2.urlopen('http://my.sina.com.cn')
            # print a,'-----a',b,'bbb---bbb',c,'ccc-ccc'
            # print BeautifulSoup(d,'html5lib').text
            # print BeautifulSoup(e,'html5lib').text
            # print BeautifulSoup(f,'html5lib').text
            # print BeautifulSoup(g,'html5lib').text
        else:
            print responseLoginJson['retcode']
            print responseLoginJson['reason']#the reason why fialed to login



    def _webread(self,url1):
        request=urllib2.Request(headers=self.header,url=url1)
        data=urllib2.urlopen(request).read()
        # print data
        return data


    def webread(self,url1):
        request = urllib2.Request(headers=self.header, url=url1)
        response = urllib2.urlopen(request)
        data=response.read()
        print response.url
        return data,response


def mainlogin():
    a=sinaLogin(username='passager%40163.com',password='ll13715325265')
    a.initPara()
    a.enableCookie()#1
    a.getPreLoginJS()#2
    a.getPostData()
    print a.username.replace('\n','')
    print a.password.replace('\n','')
    a.login()
    # a.webread('http://blog.sina.com.cn/s/blog_4d89b8340102xic5.html#cre=mysinapc&mod=f&loc=1&r=15&doct=0&rfunc=23')

if __name__ == '__main__':
    mainlogin()