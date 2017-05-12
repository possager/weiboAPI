import urllib2
import cookielib
import urllib
import random
import time



headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
}

cookies=cookielib.MozillaCookieJar()
cookiehandler=urllib2.HTTPCookieProcessor(cookies)

request=urllib2.Request(url='http://weibo.com/?category=10011')

openner=urllib2.build_opener(cookiehandler)
response=openner.open(request)
# print response
print cookies
for i in cookies:
    print '-------',i

print response.headers

print '-------------------------------------------------------------'
headers={
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    'referer':'https://login.sina.com.cn/signup/signin.php?entry=sso'
}

request2=urllib2.Request(url='https://passport.weibo.com/js/visitor/mini_original.js?v=20161116',headers=headers)
time1=time.time()

response2=openner.open(request2)
print response2.url



print time1
url3='https://login.sina.com.cn/cgi/pin.php?r=23195615&s=0'
time2=time.time()

#https://passport.weibo.com/visitor/visitor?a=restore&cb=restore_back&from=weibo&_rand=0.21129513884539497
print url3
request3=urllib2.Request(headers=headers,url=url3)
response3=openner.open(request3)
print response3.url
print response3.headers
print cookies
for i in cookies:
    print '----',i
print time2-time1
# requestend1=urllib2.Request(url='http://weibo.com/login.php',headers=headers)
# responseend=openner.open(requestend1)
# requestend2=urllib2.Request(url='http://www.weibo.com/?category=0',headers=headers)
# responseend2=openner.open(requestend2)
# print responseend2.read()

