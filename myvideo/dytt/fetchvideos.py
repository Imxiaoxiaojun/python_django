# coding=utf-8 
import urllib2
import logging
import re
#import models
from bs4 import BeautifulSoup
import base64
basepath = u'http://www.dytt8.net'
indexurl = u'http://www.ygdy8.net/index.html'
def gettypelist(url):
	typeList = []
	try:
		rep = urllib2.urlopen(urllib2.Request(url))
		if(rep.code!=200):
			print('html rep code error')
			logger.error('html rep code error')
		html = rep.read().decode('gbk','ignore')
		soup = BeautifulSoup(html,'lxml')
		typelist = soup.find_all('div',class_='co_content2')[0].contents[1].contents[1].contents
		for i in range(0,len(typelist)):
			print(typelist[i])
		#print(typelist)
		#for i in range(1,8):
			#print(typelist[i])
			#typeList.append(basepath + typelist[i].contents[1].get('href'))
	except Exception, e:
		print(e.message)
	return typeList

def getpagelist(url):
	print('getpagelist------------'+url)
	pageList = []
	try:
		rep = urllib2.urlopen(urllib2.Request(url))
		if(rep.code!=200):
			print('html rep code error')
		html = rep.read().decode('gbk','ignore')
		soup = BeautifulSoup(html,'lxml')
		pageList = soup.find_all('option',text=re.compile('[\d]'))
		for string in pageList:
			print(string)
	except Exception, e:
		print(e.message)
	return pageList 

def startfetchjob():
	typelist = gettypelist(u'http://www.ygdy8.net/html/gndy/oumei/index.html')

if __name__ == '__main__':
	startfetchjob()
	#gettypelist(u'http://www.ygdy8.net/index.html')
	#getpagelist(u'http://www.ygdy8.net/html/gndy/china/index.html')
