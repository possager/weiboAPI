#_*_coding:utf-8_*_
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
import time
import random
import pymongo





class sinaLogin:

    def __init__(self,username=None,password=None):
        self.username=username
        self.password=password
        self.header=None
        self.cookie=None
        self.openner=None
        self.client=pymongo.MongoClient('localhost',27017)
        self.COL=self.client['WeiboLogin']
        self.cookieDOC=self.COL['cookieDoc']


    def initPara(self):
        self.header={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        return self


    def getPreLoginJS(self):
        url='http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)'
        response=self.openner.open(url).read()
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
            self.openner=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler,proxy_support)
        else:
            self.openner=urllib2.build_opener(self.cookieHandler,urllib2.HTTPHandler)
        # urllib2.install_opener(openner)
        # urllib2.install_opener(openner)

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
            'vsnf': '1',

        }
        return self


    def login(self):
        loginURL='https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_='+str(int(time.time()*1000))

        #-------------------5-12
        #这次在一开始就直接加入验证码输入框,因为一开始输入验证的话至少还有提示说验证码错误.而之后再处理验证码,则总是不对.
        #而这次添加在第一次访问时请求验证码就能登录成功,可能与我这个账号本来需要验证码登录有关,如果将来不需要验证码登录的话,就知道这种
        #   继续请求验证码的方法会不会导致错误.
        headersimg = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'referer': 'https://login.sina.com.cn/signup/signin.php?entry=sso'
        }
        imageresponse = self.openner.open(
            urllib2.Request(url='https://login.sina.com.cn/cgi/pin.php?' + str(random.randint(10000000, 99999999)),
                            headers=headersimg)).read()
        timeimg=time.time()
        print int(timeimg*1000)
        with open('/media/administrator/3804CCCA04CC8C76/project/weiboAPI/YZM' + str(
                int(timeimg * 1000)) + '#' + '.png', 'w+') as imgfl:
            imgfl.write(imageresponse)
        imgfl.close()
        yanzhengma = raw_input('请输入验证码')
        print yanzhengma
        self.postdata['door'] = yanzhengma.encode('utf-8')

        #------登录成功!!!



        request1=urllib2.Request(headers=self.header,url=loginURL,data=urllib.urlencode(self.postdata))
        responseInLogin=self.openner.open(request1)


        responsedataLogin=responseInLogin.read()
        responseLoginJson=json.loads(responsedataLogin)
        print '-------',responsedataLogin
        print responseInLogin.url
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

            # -----------------5-12
            cookiedict = {}  # 用来在下边生成字典,再存在mongodb中
            for i in self.cookie:
                cookiedict[i.name] = i.value

            cookiedict['ownner'] = '17082779265'  # 以后根据这个字段来更新
            cookiedict['pwd'] = 'a123456'
            self.cookieDOC.update({'ownner': cookiedict['ownner']}, {'$set': cookiedict}, upsert=True)
            # --------


        else:
            #这下边的代码效果不保证,一般正常情况下肯定失败.
            print responseLoginJson['retcode']
            print responseLoginJson['reason']#the reason why fialed to login

            headersimg={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
                'referer': 'https://login.sina.com.cn/signup/signin.php?entry=sso'
            }
            imageresponse=self.openner.open(urllib2.Request(url='https://login.sina.com.cn/cgi/pin.php?'+str(random.randint(10000000,99999999)),headers=headersimg)).read()
            ULONG_IMG=None
            for i in self.cookie:
                print i.value
                ULONG_IMG=i.value
            timeimg=time.time()
            print timeimg
            with open('/media/administrator/3804CCCA04CC8C76/project/weiboAPI/YZM'+str(int(timeimg*1000))+'#'+ULONG_IMG+'.png','w+') as imgfl:
                # for i in imageresponse:
                #     imgfl.write(i)
                imgfl.write(imageresponse)
            imgfl.close()

            yanzhengma=raw_input('请输入验证码')
            print yanzhengma
            self.postdata['door']=yanzhengma.encode('utf-8')
            self.header['Cookie']='ULOGIN_IMG='+ULONG_IMG
            self.header['referer']='https://login.sina.com.cn/signup/signin.php?entry=sso'
            self.header['Accept-Encoding']='gzip, deflate, br'
            self.header['Accept-Language']='zh-CN,zh;q=0.8'
            self.header['Connection']='keep-alive'
            self.header['Content-Length']=531
            self.header['Content-Type']='application/x-www-form-urlencoded'
            self.header['Host']='login.sina.com.cn'
            self.header['Accept']='*/*'



            # print self.header
            # print self.postdata
            self.login()



    def _webread(self,url1):
        request=urllib2.Request(headers=self.header,url=url1)
        data=self.openner.open(request).read()

        # print data
        return data


    def webread(self,url1):
        request = urllib2.Request(headers=self.header, url=url1)
        response = self.openner.open(request)
        data=response.read()
        print response.url
        return data,response


def mainlogin():
    a=sinaLogin(username='17082779265',password='a123456')
    a.initPara()
    a.enableCookie()#1
    a.getPreLoginJS()#2
    a.getPostData()
    print a.username.replace('\n','')
    print a.password.replace('\n','')
    print a.cookie
    # for i in a.cookie:
    #     print a
    # file1=file('weibocookie.txt','a+')
    # with open(file1,mode='a+') as fl:
    #     fl.write(dict(a.cookie))
    a.login()
    print a.webread('http://blog.sina.com.cn/s/blog_4d89b8340102xic5.html#cre=mysinapc&mod=f&loc=1&r=15&doct=0&rfunc=23')



if __name__ == '__main__':
    mainlogin()