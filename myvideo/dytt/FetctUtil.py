# -*- coding:utf-8 -*-
import urllib2
import re
from bs4 import BeautifulSoup
import os
from Graph import Graph


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
        rep = urllib2.urlopen(urllib2.Request(url))
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
        resp = urllib2.urlopen(urllib2.Request(url))
        if resp.code != 200:
            return url_list
        html = resp.read().decode("utf-8", "ignore")
        url_list.extend(re.findall('<a.* href=[\',\"](.*?)[\',\"].*>.*</a>', html))
        return url_list

    @staticmethod
    def url_format(url):
        if str(url).endswith("/"):
            url += "index.jsp"
        elif str(url).startswith("/"):


    def start_fetch(self, root_url):
        self.graph.add_node([root_url])
        cur_depth = 1
        while len(self.graph.readyList) > 0:
            url = self.graph.get_node()
            if cur_depth <= self.graph.max_dept:
                url_list = self.get_url_list(url)
                self.graph.depth_size[cur_depth] = len(self.graph.readyList)
                self.graph.add_node(list(set(url_list)), filter_list, self.url_format)
                cur_depth += 1
            keys = self.graph.depth_size.keys()
            self.graph.depth_size.v
            for key in keys:
                if self.graph.depth_size[key] == len(self.graph.readyList):
                    cur_depth = key
                    break


if __name__ == "__main__":
    fetch = FetchUtil('http://www.tjgp.gov.cn/', 4)
    filter_list = ["http://www.tjgp.gov.cn/index.jsp", "http://www.tjgp.gov.cn/", "/", "#", "/index.jsp"]
    fetch.start_fetch('http://www.tjgp.gov.cn/index.jsp')
    # domain = 'http://www.watchmen.cn/'
    # fetchUtil = FetchUtil('http://www.watchmen.cn/information/', 'E:\zhuyajun\py_img\watchmen\\')
    # fetchUtil.download_img('.jpg', fetchUtil.get_image())
    # root_url = "http://www.tjgp.gov.cn/"
    # util = FetchUtil(root_url, None)



