# -*- coding:utf-8 -*-
import urllib2
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')


def gethtml(url, count):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        try:
            data = response.read().decode('gbk')
        except:
            print('异常')
            if count < 3:
                data = gethtml(url, count + 1)
            else:
                data = None
        if data:
            return data
    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason


def analyze_data(url_data, match_re):
    pong = re.compile(match_re)
    result = pong.findall(url_data)
    return result
