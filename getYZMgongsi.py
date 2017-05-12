import urllib2
import time
import random



headers={
    'User-Agnet':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
}

openner=urllib2.build_opener()
for i in range(10000):
    request=urllib2.Request(url='http://192.168.100.123:8086/ascx/ValidateCodeHandler.ashx?'+str(random.randint(10000,999999))+'.'+str(random.randint(1000000000,9999999999))+'?',headers=headers)

    print request.get_full_url()
    imageresponse=openner.open(request).read()
    timeimg=time.time()
    print timeimg

    with open('/media/administrator/3804CCCA04CC8C76/project/gongsiYZM/YZM'+str(int(timeimg*1000))+'.jpeg','w+') as imgfl:
        imgfl.write(imageresponse)
    imgfl.close()