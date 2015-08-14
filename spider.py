#!/usr/bin/env python
#coding: utf-8

import urllib
import urllib2
import cookielib
import string
import random
import re

hosturl = 'http://www.maiziedu.com'
posturl = 'http://www.maiziedu.com/user/login/'

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)

def randomString(length):
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

csrftoken = randomString(32)
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.130 Safari/537.36',
    'Referer': 'http://www.maiziedu.com/',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'csrftoken=' + csrftoken + ';',
}

postData = {
    'csrfmiddlewaretoken': csrftoken,
    'account_l': '',
    'password_l': '',
}

postData = urllib.urlencode(postData)
request = urllib2.Request(posturl, postData, headers)
response = opener.open(request)
text = response.read()
user_center_url = eval(text)['url']

##########################
course_url = 'http://www.maiziedu.com/course/python/'
course_code = opener.open(course_url).read()
course_lst = re.findall(r'(?<=lead-img">)[^>]+', course_code)

lst = []
for item in course_lst:
    tmp = re.findall(r'(?<=href=")[^"]+', item)
    if tmp:
        lst += tmp
print len(lst)
print lst

