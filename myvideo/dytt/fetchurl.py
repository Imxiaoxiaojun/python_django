# -*- coding: utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
from BloomFilter import BloomFilter
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
def geturllist(url):
    urllist = []
    # timeouttime = 1
    try:
        if bloom.__contains__(url):
            # print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------不能重复爬取'
            # errorlog.flush()
            return urllist
        bloom.add(url)
        rep = urllib2.urlopen(urllib2.Request(url), timeout=30)
        if rep.code != 200:
            print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------页面请求响应码错误'
            errorlog.flush()
            return urllist
        html = rep.read().decode('GBK', 'ignore')
        soup = BeautifulSoup(html, 'lxml')
        print >> urllog, str(threading.currentThread().getName()) + '-------' + url + '---------' + soup.title.string
        urllog.flush()
        hrefList = soup.find_all('a', href=re.compile('.{3,}'))
        pageList = soup.find_all('option', text=re.compile('[\d]'))
        formatlist(url[0:url.rfind('/')+1], pageList, 'page')
        if not set(global_pagelist) > set(pageList):
            preList.extend(pageList)
            global_pagelist.extend(pageList)
        formatlist(url[0:url.rfind("/") + 1], hrefList, 'href')
        preList.extend(hrefList)
        urllist = soup.find_all('a', href=re.compile('ftp://(.*)'))
    except Exception, e:
        # if e == 'timed out':
        #     timeouttime += 1
        #     geturllist(url)
        print >> errorlog, str(threading.currentThread().getName()) + '--' + str(url) + '-geturllist-爬取程序错误', e
        errorlog.flush()
    return urllist

def formatlist(curdomain,list,type):
    try:
        if len(list) <= 0:
            return
        if type == 'href':
            count = len(list) - 1
            while count >= 0:
                if list[count].get('href').startswith('list_') or list[count].get('href').startswith('ftp://'):
                    del list[count]
                count -= 1
        elif type == 'page':
            for i in range(0, len(list)):
                if list[i].get('value').startswith('list_'):
                    print >> errorlog, str(threading.currentThread().getName()) + '-----分页url----' + list[i].get('value')
                    errorlog.flush()
                    list[i]['value'] = curdomain + list[i].get('value')
    except Exception, e:
        print >> errorlog, str(threading.currentThread().getName()) + '-----formatlist错误----', e
        errorlog.flush()

def printFtpurl(list):
    try:
        for url in list:
            print >> ftplog, str(threading.currentThread().getName()) + '-------' + str(url)
            ftplog.flush()
    except Exception, e:
        print >> errorlog, str(threading.currentThread().getName()) + '----------printFtpurl------爬取程序错误', e
        errorlog.flush()

def getCurNum():
    global curNum
    curNum += 1
    return curNum

def foreach():
    while len(preList) > 0:
        try:
            url = preList.pop(0)
            if not isinstance(url, basestring) and None is url.get('value'):
                url = url.get('href')
            else:
                url = url.get('value')
            if not url.startswith('http://www.ygdy8.net'):
                if url.startswith('http') or url.startswith('ftp://'):
                    print >> passlog, str(threading.currentThread().getName()) + '--------跳过该url-------' + url
                    passlog.flush()
                    continue
                url = root_url + url
            if url.endswith('/'):
                url += 'index.html'
            ftpList = geturllist(url)
            if len(ftpList) > 0:
                printFtpurl(ftpList)
        except Exception, e:
            print >> errorlog, str(threading.currentThread().getName()) + '-----foreach-----爬取程序错误', e
            errorlog.flush()
        finally:
            print >> urllog, str(threading.currentThread().getName()) + '-------已经爬取' + str(getCurNum()) + '个url，待爬取url列表数量为：' + str(len(preList))
            urllog.flush()

def save(url,title):
    print(str(title)+"=================="+url)

if __name__ == '__main__':
    urllog = open('./urls.log', 'a+')
    errorlog = open('./error.log', 'a+')
    ftplog = open('./ftps.log', 'a+')
    passlog = open('./passurl.log', 'a+')
    preList = []
    global_pagelist = []
    bloom = BloomFilter(1600000, 10000)
    root_url = 'http://www.ygdy8.net/'
    curNum = 0
    geturllist('http://www.ygdy8.net/index.html')
    foreach()
    urllog.close()
    errorlog.close()
    ftplog.close()
    passlog.close()

