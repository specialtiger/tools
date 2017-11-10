#-*- coding:utf-8 -*-
import urllib2 as url_req
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#2.urllib库 + json库的json.loads()
url = 'http://api.map.baidu.com/telematics/v3/weather?location=%E5%B9%BF%E5%B7%9E&output=json&ak=KPGX6sBfBZvz8NlDN5mXDNBF&callback='
#注意必须要.decode('utf8')，不然会有错误：the JSON object must be str, not 'bytes'
request = url_req.urlopen(url).read()
s = json.loads(request)
print request
print("查询日期："+s['date'])
print("城市："+s['results'][0]['currentCity'])
print("pm2.5值："+s['results'][0]['pm25'])
print("\n")
for i in range(0,4):
    print("日期："+s['results'][0]['weather_data'][i]['date'])
    print("天气："+s['results'][0]['weather_data'][i]['weather'])
    print("风力："+s['results'][0]['weather_data'][i]['wind'])
    print("温度："+s['results'][0]['weather_data'][i]['temperature'])
    print("---------------")
