#!/usr/bin/env python
#coding: utf-8

import urllib
import urllib2
import cookielib
import string
import random
import re
from bs4 import BeautifulSoup
import sys 
reload(sys) 
sys.setdefaultencoding("utf-8")

hosturl = 'http://www.maiziedu.com'
posturl = 'http://www.maiziedu.com/user/login/'

def randomString(length):
    return ''.join(random.choice(string.letters + string.digits) for i in xrange(length))

def opener():
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    return opener
    
def login(username, password):
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
        'account_l': username,
        'password_l': password,
    }
    postData = urllib.urlencode(postData)
    request = urllib2.Request(posturl, postData, headers)
    text = opener().open(request).read()
    user_center_url = eval(text)['url']
    return user_center_url

def getallcourse():
    course_lst = []
    mainpage = opener().open(hosturl).read()
    soup = BeautifulSoup(mainpage, 'html.parser')
    souplilst = soup.find(name='div', attrs={'class':'ind-cour-box'}).ul.findAll('li')
    for item in souplilst:
        course_lst.append(hosturl + item.a['href'])
    return course_lst


def getlessons(url): 
    href = []
    #title = []
    content = opener().open(url).read()
    course_lst = re.findall(r'(?<=lead-img">)[^>]+', content)
    
    for item in course_lst:
        href += re.findall(r'(?<=href=")[^"]+', item)
        #title += re.findall(r'(?<=title=")[^"]+', item)
    return href
    
def getsections(url):
    content = opener().open(url).read()
    soup = BeautifulSoup(content, 'html.parser')
    playlist = soup.find(name='div', attrs={'id': 'playlist'}).ul.findAll('li')
    for item in playlist:
        print item.a['href'], item.a.text
        print BeautifulSoup(opener().open(hosturl + item.a['href'])).find(name='video', attrs={'id': 'microohvideo'}).source['src']


if __name__ == '__main__':
    login('', '')
    #course_lst = getallcourse()
    course_url = hosturl + '/course/python/'
    lessons = getlessons(course_url)
    getsections(hosturl+lessons[0])
