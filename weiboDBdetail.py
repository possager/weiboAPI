#_*_coding:utf-8_*_
import pymongo

class bangdan24:
    def __init__(self):
        self.mid=None
        self.username=None
        self.persional_certificate=False
        self.is_vip=False
        self.forum_url=None
        self.user_id=None
        self.publish_time=None
        self.come_from=None
        self.user_homepage=None
        self.content=None

        self.client=pymongo.MongoClient('localhost',27017)
        self.DB=self.client['Weibocontent']
        self.COL=self.DB['bangdan24']


    def InitialDB(self):
        self.COL.create_index([('publish_time',pymongo.ASCENDING),('mid',pymongo.DESCENDING)],unique=True)

    def deal(self):
        dict1={
            'mid':self.mid,
            'username':self.username,
            'persional_certificate':self.persional_certificate,
            'is_vip':self.is_vip,
            'forum_url':self.forum_url,
            'user_id':self.user_id,
            'publish_time':self.publish_time,
            'come_from':self.come_from,
            'user_homepage':self.user_homepage,
            'content':self.content
        }

        self.COL.insert(dict1)

    def DBshow(self):
        print '<热榜24小时数据库>数量---------->',self.COL.find().count()