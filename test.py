from weibo import APIClient
import dataEncode
import webbrowser
import urllib2
import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import json
import ssl

APP_KEY='922763770'
APP_SECRET='0ee74c72b699d61d2f7062ec8034496c'
CALLBACK='http://www.baidu.com'

client=APIClient(app_key=APP_KEY,app_secret=APP_SECRET,redirect_uri=CALLBACK)
url=client.get_authorize_url()
print url
aaa=time.time()
# a=webbrowser.open(url)

# request=client.request_access_token('de7a0d762b801f6160ce6007987ceb85'
#                                     )
# access_token=request.access_token
# expires_in=request.expiress_in
# client.set_access_token(access_token,expires_in)
# client.statuses.updata.post(statues=u'Test OAuth 2.0 Send a Weibo!')

chrome=webdriver.Chrome()
chrome.get(url)
chrome.find_element_by_id('userId').send_keys('passager@163.com')
chrome.find_element_by_id('passwd').send_keys('ll13715325265')
time.sleep(0.6)
chrome.find_element_by_css_selector('#outer > div > div.WB_panel.oauth_main > form > div > div.oauth_login_box01.clearfix > div > p > a.WB_btn_login.formbtn_01').click()
time.sleep(2)
print chrome.current_url
url2=chrome.current_url
chrome.close()
bbb=time.time()
print bbb-aaa
code=url2.split('code=')[1]
r=client.request_access_token(code)
# print help(r)
accesstoken=r.get('access_token')
print r.keys()
expiresin= r.get('expires_in')
# print r.get('uid')
# print r.get('expires')
# client.set_access_token(access_token=accesstoken,expires=expiresin)
#
# print client.statuses.user_timeline.get()
# print client.user.show.get()

data={
    'access_token':accesstoken
}
print accesstoken
url3='https://api.weibo.com/2/statuses/user_timeline/ids.json?access_token='+accesstoken
# request1=urllib2.urlopen(url3,data=data,context=ssl._create_default_https_context)
request1=requests.get(url3,verify=False).content
print request1