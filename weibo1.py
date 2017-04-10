# !/usr/bin/env python
# -*- coding: utf-8 -*-

from weibo import APIClient
import webbrowser  # python内置的包

APP_KEY='922763770'
APP_SECRET='0ee74c72b699d61d2f7062ec8034496c'
CALLBACK_URL='http://www.baidu.com'

# 利用官方微博SDK
client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
# 得到授权页面的url，利用webbrowser打开这个url
url = client.get_authorize_url()
print url
webbrowser.open_new(url)
# 获取code=后面的内容
print '输入url中code后面的内容后按回车键：'
code = raw_input()
# code = your.web.framework.request.get('code')
# client = APIClient(app_key=APP_KEY, app_secret=APP_SECRET, redirect_uri=CALLBACK_URL)
r = client.request_access_token(code)
access_token = r.access_token  # 新浪返回的token，类似abc123xyz456
expires_in = r.expires_in
# 设置得到的access_token
client.set_access_token(access_token, expires_in)

# 可以打印下看看里面都有什么东西
# print client.statuses__public_timeline()
statuses = client.statuses__public_timeline()['statuses']
length = len(statuses)
# 输出了部分信息
for i in range(0, length):
    print u'昵称：' + statuses[i]['user']['screen_name']
    print u'简介：' + statuses[i]['user']['description']
    print u'位置：' + statuses[i]['user']['location']
    print u'微博：' + statuses[i]['text']



# from weibo import APIClient
# import webbrowser
#
# APP_KEY='2610508406'
# APP_SECRET='8fc017413e91c0f5ce9fc48409c9e367'
# CALLBACK_URL='www.baidu.com'
#
# client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK_URL)
# url=client.get_authorize_url()
# print url
# webbrowser.open(url)
# print 'please input the code behind url'
# code=raw_input()
# r=client.request_access_token(code)
# access_token=r.access_token