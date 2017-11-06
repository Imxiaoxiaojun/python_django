# -*- coding:utf-8 -*-
import urllib2
from pybloom import BloomFilter
from bs4 import BeautifulSoup
import os
from Graph import Graph
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class FetchUtil(object):
    def __init__(self, domain, max_depth, doc_path=None):
        self.domain = domain
        self.graph = Graph(max_depth)
        if doc_path is not None:
            if not os.path.exists(doc_path):
                os.makedirs(doc_path)
            self.image_path = doc_path

    @staticmethod
    def get_image(url):
        image_list = []
        rep = urllib2.urlopen(urllib2.Request(url), timeout=30)
        if rep.code != 200:
            return image_list
        html = rep.read().decode('utf-8', 'ignore')
        soup = BeautifulSoup(html, 'lxml')
        image_list = soup.find_all('img', class_='tn')
        return image_list

    def download_img(self, img_type, img_list):
        for i in range(len(img_list)):
            # filename = self.image_list[i]['src'].split("/")[-1]
            response = urllib2.urlopen(urllib2.Request(self.domain + img_list[i]['src']))
            if response.code != 200:
                continue
            with open(self.image_path + str(i) + img_type, "wb") as f:
                f.write(response.read())

    @staticmethod
    def get_url_list(url):
        url_list = []
        try:
            if bloom.__contains__(url):
                return url_list
            bloom.add(url)
            resp = urllib2.urlopen(urllib2.Request(url))
            if resp.code != 200:
                return url_list
            html = resp.read().decode("utf-8", "ignore")
            soup = BeautifulSoup(html, "lxml")
            url_list.extend(soup.find_all("a"))
        except Exception, e:
            print url, e
        return url_list

    def url_format(self, url):
        if url.get("href"):
            url = url.get("href")
        if url in filter_list or url in self.graph.readyList:
            return None
        elif str(url).startswith("http") and not str(url).startswith(self.domain):
            return None
        elif str(url).endswith("/"):
            url += u_main_page
        elif str(url).startswith("/"):
            url = self.domain + url
        elif str(url).startswith("?"):
            url = self.domain + "/portal/topicView.do" + url
        else:
            return None
        return url

    def start_fetch(self, root_url):
        self.graph.add_node([root_url])
        cur_depth = 1
        print "fetching。。。"
        while len(self.graph.readyList) > 0:
            url = self.graph.get_node()
            print "Number of queues to fetch：", len(self.graph.readyList)
            if url is None:
                continue
            if cur_depth <= self.graph.max_dept:
                print >> url_log, "深度-------", cur_depth, "url-------"+url
                url_log.flush()
                url_list = self.get_url_list(url)
                self.graph.depth_size[cur_depth] = len(self.graph.readyList)
                self.graph.add_node(list(set(url_list)), self.url_format)
                cur_depth += 1
            keys = self.graph.depth_size.keys()
            for key in keys:
                if self.graph.depth_size[key] == len(self.graph.readyList):
                    cur_depth = key
                    break


if __name__ == "__main__":
    url_log = open('./urls.log', 'a+')
    bloom = BloomFilter(capacity=10000000, error_rate=0.0001)
    try:
        u_domain = input("please input domain(\"http://www.tjgp.gov.cn/\"):\n")
        while str(u_domain).strip() == "":
            u_domain = input()
        u_main_page = input("please input index page（\"/index.jsp\"） \n")
        while str(u_main_page).strip() == "":
            u_main_page = input()
    except Exception, e:
        print e
    fetch = FetchUtil(u_domain, 4)
    filter_list = [u_domain, "/", "#", u_main_page]
    fetch.start_fetch(u_domain)
    url_log.close()
    print "complete!"




