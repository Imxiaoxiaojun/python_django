# -*- coding: utf-8 -*-
import urllib2
import re
from pybloom import BloomFilter
import threading
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def geturllist(url):
    try:
        lock.acquire()
        if bloom.__contains__(url):
            print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------不能重复爬取'
            errorlog.flush()
            lock.release()
            return
        bloom.add(url)
        lock.release()
        rep = urllib2.urlopen(urllib2.Request(url), timeout=30)
        if rep.code != 200:
            print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------页面请求响应码错误'
            errorlog.flush()
            return
        html = rep.read().decode('GBK', 'ignore')
        titlenmae = re.findall('<title>(.*?)</title>', html)[0]
        print >> urllog, str(threading.currentThread().getName()) + '-------' + url + '---------' + titlenmae
        urllog.flush()
        ftplist = re.findall('<a.* href=[\',\"](ftp:.*?)[\',\"].*>.*</a>', html)
        if len(ftplist) > 0:
            printFtpurl(ftplist)
            return
        hrefList = re.findall('<a.* href=[\',\"](.*?)[\',\"].*>.*</a>', html)
        lock.acquire()
        formatlist(url[0:url.rfind("/") + 1], hrefList)
        global preList
        preList = list(set(preList + hrefList))
        lock.release()
    except Exception, e:
        print >> errorlog, str(threading.currentThread().getName()) + '--' + str(url) + '-geturllist-爬取程序错误', e
        errorlog.flush()


def formatlist(curdomain,hreflist):
    try:
        if len(hreflist) <= 0:
            return
        for j in range(len(hreflist)):
            if hreflist[j].startswith('list_'):
                hreflist[j] = curdomain + hreflist[j]
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
    lock.acquire()
    global curNum
    curNum += 1
    lock.release()
    return curNum


def foreach():
    while len(preList) > 0:
        try:
            lock.acquire()
            url = preList.pop(-1)
            lock.release()
            if None is url:
                break
            if not url.startswith('http://www.ygdy8.net'):
                if (url.startswith('http') and not url.endswith('.exe')) or url.startswith('ftp://'):
                    print >> passlog, str(threading.currentThread().getName()) + '--------跳过该url-------' + url
                    passlog.flush()
                    continue
                elif url.startswith('http') and (url.endswith('.exe') or url.endswith('.rar')):
                    print >> ftplog, str(threading.currentThread().getName()) + '-------' + str(url)
                    ftplog.flush()
                    continue
                url = root_url + url
            if url.endswith('/'):
                url += 'index.html'
            geturllist(url)
        except Exception, e:
            print >> errorlog, str(threading.currentThread().getName()) + '-----foreach-----爬取程序错误', e
            errorlog.flush()
        finally:
            print >> urllog, str(threading.currentThread().getName()) + '-------已经爬取' + str(getCurNum()) + '个url，待爬取url列表数量为：' + str(len(preList))
            urllog.flush()


if __name__ == '__main__':
    urllog = open('./urls.log', 'a+')
    errorlog = open('./error.log', 'a+')
    ftplog = open('./ftps.log', 'a+')
    passlog = open('./passurl.log', 'a+')
    preList = []
    global_pagelist = []
    bloom = BloomFilter(capacity=10000000, error_rate=0.0001)
    root_url = 'http://www.ygdy8.net/'
    curNum = 0
    thread_list = []  # 线程存放列表
    lock = threading.RLock()
    startNum = 0
    geturllist('http://www.dy2018.com/index.html')
    if len(preList) <= 0:
        sys.exit()
    for i in range(20):
        t = threading.Thread(target=foreach)
        t.setDaemon(True)
        thread_list.append(t)
    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()
    urllog.close()
    errorlog.close()
    ftplog.close()
    passlog.close()

