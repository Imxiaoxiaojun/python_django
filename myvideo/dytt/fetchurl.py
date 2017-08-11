#coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup
from BloomFilter import BloomFilter
def geturllist(url):
    urllist = []
    try:
        rep = urllib2.urlopen(urllib2.Request(url),timeout=5)
        if(rep.code!=200):
            return urllist
        html = rep.read().decode('GBK','ignore')
        soup = BeautifulSoup(html,'lxml')
        #print(url +"------------"+ soup.title.string)
        #save(url,soup.title.string)
        hreflist = soup.find_all('a',href=re.compile("[10,100]"))
        urllist.extend(hreflist)
    except Exception,e:
        print (url)
        print(e.message)
    return urllist

def foreach(url,num):
    try:
        if (num  > maxnum):
            return
        num+=1
        list = geturllist(url)
        print(len(list))
        if (len(list)<=0 or num-1 == maxnum):
            return
        for i in range(len(list)):
            try:
                #save(root_url + list[i].get("href"),i)
                url = list[i].get("href")
                if url.startswith("ftp://"):
                    print url
                elif(url.find("http://www.dy2018.com") == -1):
                    url = root_url + list[i].get("href")
                if not bloom.__contains__(url):
                    #print(str(i)+"------num---"+str(num-1)+"---------"+url)
                    bloom.add(url)
                    foreach(url,num)
            except Exception,e:
                print ("foreach error")
    except Exception,e:
        print(e.message)

def save(url,title):
    print(str(title)+"=================="+url)
if __name__ == '__main__':
    maxnum = 1000
    bloom = BloomFilter(160000,1000)
    bloom.add('http://www.dy2018.com/index.html')
    bloom.add('http://www.dy2018.com/')
    root_url = 'http://www.dy2018.com'
    foreach('http://www.dy2018.com/index.html',1)
