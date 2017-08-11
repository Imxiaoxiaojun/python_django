#coding=utf-8
import urllib2 
from bs4 import BeautifulSoup
def geturllist(url):
    urllist = []
    try:
        rep = urllib2.urlopen(url)
        if(rep.code!=200):
            return urllist
        html = rep.read().decode('GBK','ignore')
        soup = BeautifulSoup(html,'lxml')
        save(url,soup.title.string)
        hreflist = soup.find_all('a')
        urllist.extend(hreflist)
    except Exception,e:
        print(e.message)
    return urllist

def foreach(url,num):
    if(num>2):
        return
    try:
        num+=1
        list = geturllist(url)
        if (len(list)<=0):
            return
        for i in range(len(list)):
            try:
                foreach(root_url + list[i].get("href"),num)
            except Exception,e:
                print ("foreach error")
    except Exception,e:
        print(e.message)

def save(url,title):
    print(url+"----"+title)
if __name__ == '__main__':
    root_url = u'http://www.dy2018.com/'
    foreach(u'http://www.dy2018.com/',1)
