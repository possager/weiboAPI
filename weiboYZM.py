import urllib2
import requests
import time
import random
import cookielib




class weiboYZM:
    def __init__(self):
        headers={
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            }
        cookie=cookielib.LWPCookieJar()

    # def open