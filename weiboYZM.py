#_*_coding:utf-8_*_
import urllib2
import requests
import time
import random
import cookielib
import pymongo
from bs4 import BeautifulSoup
import json
import re
from weiboDBdetail import bangdan24



class weiboYZM:
    def __init__(self):

        self.headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            }
        self.cookie=cookielib.LWPCookieJar()
        self.cookiehandler=urllib2.HTTPCookieProcessor(self.cookie)
        self.client=pymongo.MongoClient('localhost',27017)
        self.COL=self.client['WeiboLogin']
        self.cookieDOC=self.COL['cookieDoc']



    def _Init(self):
        dict1=self.cookieDOC.find_one({},{'_id':0,'ownner':0,'pwd':0})
        cookiestr=''
        for i in dict1:
            cookiestr+=(i+'='+dict1[i]+';')
        print cookiestr
        self.headers['cookie']=cookiestr
        print self.headers

    def run(self):
        self._Init()
        self.openner=urllib2.build_opener(self.cookiehandler)
        for i in range(1):
            time.sleep(random.randint(2,5))
            url1='http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803&pagebar=0&tab=home&current_page='+str(i+1)+'&pre_page='+str(i)+'&page='+str(i)+'&pl_name=Pl_Core_NewMixFeed__3&id=102803&script_uri=/102803&feed_type=1&domain_op=102803'
            self.request=urllib2.Request(url=url1,headers=self.headers)



            response=self.openner.open(self.request)
            print response.url
            responsedata= response.read()


            #5-16日发现这里可能存在跳转,原因很有可能是因为cookie中的某些值过期了,要么更新cookie,要么这下边判断,然后再重新定位进入
            #重新定位不行,一定要更新cookies.也就是后边的那几个网页要依次访问了.
            #5-17微博的cookie一天就会过期

            print responsedata

            try:
                datajson = json.loads(responsedata)#如果过期就会跳转到js,加载就会失败,就会跳转到后边的更新cookie和再次登录模块
            except Exception as e:
                print e,'\n'
                #依次访问登录时会访问的3个页面,不要错过任何一个cookie
                self.request.url='http://login.sina.com.cn/crossdomain2.php?action=login'
                self.openner.open(self.request)
                self.request.url='http://i.sso.sina.com.cn/js/ssologin.js'
                self.openner.open(self.request)
                self.request.url='https://login.sina.com.cn/'
                self.openner.open(self.request)



                #dataEncode中的cookie更新代码
                cookiedict = {}
                for j in self.cookie:
                    cookiedict[j.name] = j.value
                cookiedict['ownner'] = '17082779265'  #用来判断这个cookies是谁的
                cookiedict['pwd'] = 'a123456'
                self.cookieDOC.update({'ownner': cookiedict['ownner']}, {'$set': cookiedict}, upsert=True)


                #更新headers后再访问24小时榜单的json,看看能返回什么信息
                self._Init()
                time.sleep(random.randint(2, 5))
                url1 = 'http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803&pagebar=0&tab=home&current_page=' + str(
                    i + 1) + '&pre_page=' + str(i) + '&page=' + str(
                    i) + '&pl_name=Pl_Core_NewMixFeed__3&id=102803&script_uri=/102803&feed_type=1&domain_op=102803'
                self.request = urllib2.Request(url=url1, headers=self.headers)
                response = self.openner.open(self.request)
                print response.url
                responsedata = response.read()









            datajson=json.loads(responsedata)
            datajsonsoup=BeautifulSoup(datajson['data'],'lxml')
            for i in datajsonsoup:
                print i

            for i in datajsonsoup.select('div["tbinfo"]'): #div > div.WB_feed.WB_feed_v3.WB_feed_v4
                thisclass=bangdan24()
                print '\n'
                thisclass.mid = i.get('mid')
                detail= i.select('div.WB_feed_detail.clearfix > div.WB_detail > div.WB_info > a')


                userstatus=[]
                for j in detail:
                    if j.get('title'):
                        temporary= j.get('title').encode('utf-8')
                        print temporary
                        userstatus.append(str(temporary))

                    else:
                        temporary= j.select('i')[0].get('title').encode('utf-8')
                        print '个人认证微博',temporary
                        userstatus.append(str(temporary))

                print userstatus,'----',len(userstatus)

                for j in i.select(' div.WB_feed_detail.clearfix > div.WB_detail > div.WB_from.S_txt2 > a'):
                    if j.get('name'):
                        print '帖子链接-',j.get('href')
                        print '用户id--',j.get('name')
                        print '时间----',j.get('date')
                    else:
                        print '来自----',j.text

                for j in  i.select(' div.WB_feed_detail.clearfix > div.WB_face.W_fl > div > a'):
                    print '该用户的主页',j.get('href')
                for j in i.select(' div.WB_feed_detail.clearfix > div.WB_detail > div.WB_text.W_f14'):
                    print j.text



            # for i in datajsonsoup.select('div.WB_info'):
            #     print '用户昵称-------',i.text
            #     # print '用户链接-------',i.select('a')[0].get('href')
            #     print '用户昵称2------',i.select('a')[0].get('nick-name').strip()
            #
            #
            # for i in datajsonsoup.select('div.WB_from.S_txt2 > a'):
            #     print i.get('name')
            #     if i.get('name'):
            #         print '帖子的具体链接---',i.get('href')
            #         print 'publisher_id---',i.get('name')
            #         print '发帖时间--------',i.get('date')
            #     else:
            #         print '来自客户端-------',i.text
            #
            #
            # for i in datajsonsoup.select('div.WB_text.W_f14'):
            #     print '======不知道是什么',i.text




            # fileresponse=file('/media/administrator/3804CCCA04CC8C76/project/nouse/sina/responsedata_bangdan.txt','a+')
            with open('/media/administrator/3804CCCA04CC8C76/project/nouse/sina/responsedata_bangdan.txt','a+') as fl:
                fl.write(responsedata)
            fl.close()



if __name__ == '__main__':
    a=weiboYZM()
    a.run()
    #http://d.weibo.com/p/aj/v6/mblog/mbloglist?ajwvr=6&domain=102803&pagebar=0&tab=home&current_page=1&pre_page=0&page=0&pl_name=Pl_Core_NewMixFeed__3&id=102803&script_uri=/102803&feed_type=1&domain_op=102803
    #数据源的格式
