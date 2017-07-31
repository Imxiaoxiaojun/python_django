#coding=utf-8 
import urllib2
import logging
import re
import models
from bs4 import BeautifulSoup
global basepath,pagepath,vtype,vtag
indexurl = 'http://www.dytt8.net/html/tv/oumeitv/index.html'
basepath = 'http://www.dytt8.net'
pagepath = 'http://www.dytt8.net/html/tv/oumeitv/'
vtype = 'tv'
vtag = 'omtv'
logger = logging.getLogger('django')
def main():
	try:
		pagelist = getpagelist()
		print(len(pagelist))
		if(len(pagelist)<1):
			logger.error('getpage error ,list < 1')
			return
		dbcount = models.Video.getcount({'type':vtype,'tag':vtag})
		endpage = dbcount/25 if dbcount%25 == 0 else dbcount/25 + 1
		lastpage = gettvlist(pagepath+pagelist[-1].get('value'))
		onlinecount = (len(pagelist)-1)*25+len(lastpage)
		#如果数据库数量和线上的数量一致，说明更新过了，跳过
		if(dbcount == onlinecount):
			logger.info('already refreshed')
			return 
		#数据多少页，就批量更新到数据页数的前一页，当页单挑更新
		difpage = len(pagelist) - endpage
		if(difpage>0):
			for i in range(0,difpage):
				try:
					list = gettvlist(pagepath+pagelist[i].get('value'))	
					if not(batchSave(list)):
						print('batchsave is False')
						models.FailVideo.save({'url':pagepath+pagelist[i].get('value'),'type':'pagelist'})
				except Exception, e:
					logger.error(e.message)
		singleSave(gettvlist(pagepath+pagelist[difpage].get('value')))
	except Exception,e:
		logger.error(e.message)
		

def gettvlist(url):
	print('getlist url ============================='+url)
	tvList = []
	try:
		rep = urllib2.urlopen(urllib2.Request(url))
		if(rep.code!=200):
			print('html rep code error')
			logger.error('html rep code error')
		html = rep.read().decode('gbk','ignore')
		soup = BeautifulSoup(html,'lxml')
		tvList = soup.find_all('a',class_='ulink')
	except Exception, e:
		print(e.message)
		logger.error(e.message)
	print('gettvlist result length ============='+str(len(tvList)))
	return tvList 

def getpagelist():
	pageList = []
	try:
		rep = urllib2.urlopen(urllib2.Request(indexurl))
		if(rep.code!=200):
			print('html rep code error')
			logger.error('html rep code error')
		html = rep.read().decode('gbk','ignore')
		soup = BeautifulSoup(html,'lxml')
		pageList = soup.find_all('option',text=re.compile('[\d]'))
	except Exception, e:
		print(e.message)
		logger.error(e.message)
	return pageList 


# return False or True
def batchSave(list):
	try:
		batchList = []
		for i in range(len(list)):
			surl = basepath + list[i].get('href')
			sname = list[i].string
			if(len(sname)<7):
				continue
			print(sname)
			video = models.Video(name=sname,url=surl,type=vtype,tag=vtag)
			batchList.append(video)
		models.Video.objects.bulk_create(batchList)
	except Exception, e:
		logger.error(e.message)
		return False	
	return True			

# return False or True
def singleSave(list):
	try:
		for i in range(len(list)):
			try:
				surl = basepath + list[i].get('href')
				sname = list[i].string
				if(len(sname)<7):
					continue
				print(sname)
				models.Video.objects.create(name=sname,url=surl,type=vtype,tag=vtag)
			except Exception,e:
				logger.error(e.message)
	except Exception,e:
		return False
	return True

if __name__ == '__main__':
	main()

