# -*- coding: UTF-8 -*-
import urllib2
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# 由于tkinter中没有ToolTip功能，所以自定义这个功能如下
class Test(object):
    def __init__(self):
        pass

    def fetch(self, url):
        resp = urllib2.urlopen(urllib2.Request(url))
        if resp.code != 200:
            print "return code error"

        html = resp.read().decode("UTF-8", "ignore")
        soup = BeautifulSoup(html, "lxml")
        print soup

if __name__ == "__main__":
    test = Test()
    test.fetch("http://www.tjgp.gov.cn/portal/documentView.do?method=view&id=54793001&ver=2")
