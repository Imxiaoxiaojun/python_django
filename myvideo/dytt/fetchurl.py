#coding=utf-8
import urllib2
import re
from bs4 import BeautifulSoup
from BloomFilter import BloomFilter
def geturllist(url):
    urllist = []
    try:
        if bloom.__contains__(url):
            return urllist
        bloom.add(url)
        rep = urllib2.urlopen(urllib2.Request(url),timeout=5)
        if(rep.code!=200):
            return urllist
        html = rep.read().decode('GBK','ignore')
        soup = BeautifulSoup(html,'lxml')
        strs = url + '---------' + soup.title.string
        print >> logsfile,strs.encode('utf-8')
        logsfile.flush()
        #print(url +"------------"+ soup.title.string)
        #save(url,soup.title.string)
        hreflist = soup.find_all('a',href=re.compile("[10,100]"))
        urllist.extend(hreflist)
    except Exception,e:
        return urllist
    return urllist

def foreach(url,num):
    try:
        num+=1
        if (num  > maxnum):
            return
        list = geturllist(url)
        #print(len(list))
        if (len(list)<=0):
            return
        for i in range(len(list)):
            try:
                #save(root_url + list[i].get("href"),i)
                url = list[i].get("href")
                if url.startswith("ftp://"):
                    num = maxnum
                    print >> logsfile,url.encode('utf-8')
                    logsfile.flush()
                elif(url.find("http://www.dy2018.com") == -1):
                    url = root_url + list[i].get("href")
                    #print(str(i)+"------num---"+str(num-1)+"---------"+url)
                foreach(url,num)
            except Exception,e:
                continue
                #print >> logsfile,("foreach error")
    except Exception,e:
        return
        #print >> logsfile,e.message

def save(url,title):
    print(str(title)+"=================="+url)
if __name__ == '__main__':
    maxnum = 4 
    logsfile = open('./urls.log', 'a+')
    bloom = BloomFilter(160000,1000)
    root_url = 'http://www.dy2018.com'
    foreach('http://www.dy2018.com/index.html',1)
    logsfile.close()
