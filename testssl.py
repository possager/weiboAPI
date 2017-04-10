import urllib2
from bs4 import BeautifulSoup
import html5lib
import requests
import ssl
import dataEncode
from  weibo import APIClient


ssl._create_default_https_context=ssl._create_unverified_context

APP_KEY='922763770'
APP_SECRET='0ee74c72b699d61d2f7062ec8034496c'
CALLBACK='http://www.baidu.com'

client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK)
url=client.get_authorize_url()
print url

a=dataEncode.sinaLogin(username='passager%40163.com',password='ll13715325265')
a.initPara()
a.enableCookie()  # 1
a.getPreLoginJS()  # 2
a.getPostData()
a.login()

data,response=a.webread(url)
# print data
code=response.url.split('code=')[1]
print code
r=client.request_access_token(code)
# print help(r)
accesstoken=r.get('access_token')
print r.keys()
expiresin= r.get('expires_in')
uid=r.get('uid')
print uid

weiboAPIurl='https://api.weibo.com/2/users/show.json'


data={
    'access_token':accesstoken
}
print accesstoken
url3='https://api.weibo.com/2/friendships/friends.json'+'?access_token='+accesstoken+'&uid='+uid
print url3
# request1=urllib2.urlopen(url3,data=data,context=ssl._create_default_https_context)
data3,_=a.webread(url3)
print data3



# print type(headers1)
# print headers1.keys()
# print headers1.readheaders()
# print help(headers1)
# request1=urllib2.Request('https://api.weibo.com/oauth2/authorize?redirect_uri=http%3A//www.baidu.com&response_type=code&client_id=922763770')
# openner1=urllib2.build_opener()
# data=openner1.open(request1)
# print data.read()

# data3=requests.get('https://api.weibo.com/oauth2/authorize?redirect_uri=http%3A//www.baidu.com&response_type=code&client_id=922763770').content