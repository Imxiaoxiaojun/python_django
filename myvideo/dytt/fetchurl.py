#coding=utf-8
import urllib2 
from bs4 import BeautifulSoup
class FetchUrl():
    def geturllist(url):
        urllist = []
        try:
            html = urllib2.urlopen(url).read().decode('GBK')
            soup = BeautifulSoup(html,'lxml')
            print(soup.title)
            hreflist = soup.find_all('a')
            for str in hreflist:
                print(str)
        except:
            print('error')
    def foreach(url):
        try:
            list = geturllist(url)
            if (len(list)<=0):
                return
            for i in range(len(list)):
                try:
                    #插入数据库，成功说明这条url没有爬取过，失败则跳过爬取当前的url
                    foreach(list.)
                #TODO

                #
        except:

    if __name__ == '__main__':
        root_url = 'http://www.dy2018.com/'
        geturls('http://www.dy2018.com/')
