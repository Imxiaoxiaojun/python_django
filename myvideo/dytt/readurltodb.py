# -*- coding: utf-8 -*-
from collections import Counter
from DBUtil import Mysql
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class FtpUrl(object):
    def __init__(self, name, link):
        self.Name = name
        self.Url = link


if __name__ == '__main__':
    urls = open('ftps.log')
    urllist = []
    videoList = []
    for url in urls:
        if url.rstrip() != '':
            urllist.append(url)
    urllist = list(set(urllist))

    for url2 in urllist:
        vname = url2[url2.rfind('.com]') + 5:] if url2.rfind('.com]') != -1 else url2[url2.rfind('.org]') + 5:] \
            if url2.rfind('.org]') != -1 else url2[url2.rfind('.net]') + 5:] if url2.rfind('net]') != -1 \
            else url2[url2.rfind('/') + 1:] if url2.rfind('/') != -1 else ''
        if str(vname)[0] == '.':
            vname = vname[1:]
        vurl = url2[url2.find('-------') + 7:].rstrip()
        videoList.append([str(vname).rstrip(), str(vurl).rstrip()])

    # for i in range(len(videoList)):
    #     if len(videoList[i]) > 200:
    #         print videoList[i]
    mysql = Mysql()
    # sql = "insert into ftplink (ftp_name,ftp_url) values(%s,%s)"
    # count = mysql.insertMany(sql, videoList)
    # if count == len(urllist):
    #     mysql.end('commit')
    # else:
    #     mysql.end('rollback')
