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
    try:
        if bloom.__contains__(url):
            # print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------不能重复爬取'
            # errorlog.flush()
            return urllist
        lock.acquire()
        bloom.add(url)
        lock.release()
        rep = urllib2.urlopen(urllib2.Request(url), timeout=10)
        if rep.code != 200:
            print >> errorlog, str(threading.currentThread().getName()) + '-------' + str(url) + '-----------页面请求响应码错误'
            errorlog.flush()
            return urllist
        html = rep.read().decode('GBK', 'ignore')
        soup = BeautifulSoup(html, 'lxml')
        print >> urllog, str(threading.currentThread().getName()) + '-------' + url + '---------' + soup.title.string
        urllog.flush()
        hrefList = soup.find_all('a', href=re.compile('.{3,}'))
        lock.acquire()
        preList.extend(hrefList)
        lock.release()
        urllist = soup.find_all('a', href=re.compile('ftp://(.*)'))
    except Exception, e:
        print >> errorlog, str(threading.currentThread().getName()) + '--' + str(url) + '-geturllist-爬取程序错误', e
        errorlog.flush()
    return urllist

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
            lock.acquire()
            url = preList.pop(0)
            lock.release()
            if not isinstance(url, basestring):
                url = url.get('href')
            if not url.startswith('http://www.dy2018.com'):
                if url.startswith('http'):
                    continue
                url = root_url + url
            if url.endswith('/'):
                url += 'index.html'
            print >> urllog, str(threading.currentThread().getName()) + '-------开始爬取第' + str(getCurNum()) + '个url'
            urllog.flush()
            ftpList = geturllist(url)
            if len(ftpList) > 0:
                printFtpurl(ftpList)
                urllog.flush()
        except Exception, e:
            print >> errorlog, str(threading.currentThread().getName()) + '-----foreach-----爬取程序错误' + str(e)
            errorlog.flush()
        finally:
            print >> urllog, str(threading.currentThread().getName()) + '-----------当前待爬取url列表数量为：' + str(len(preList))
            urllog.flush()

def save(url,title):
    print(str(title)+"=================="+url)

if __name__ == '__main__':
    urllog = open('./urls.log', 'a+')
    errorlog = open('./error.log', 'a+')
    ftplog = open('./ftps.log', 'a+')
    preList = []
    bloom = BloomFilter(160000, 1000)
    root_url = 'http://www.dy2018.com'
    curNum = 0
    thread_list = []  # 线程存放列表
    lock = threading.RLock()
    geturllist('http://www.dy2018.com/index.html')
    for i in range(10):
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

