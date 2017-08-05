# coding=utf-8 
import urllib2
import logging
import re
import models
from bs4 import BeautifulSoup
global basepath,pagepath,vtype,vtag,logger
indexurl = u'http://www.dytt8.net/html/tv/oumeitv/index.html'
basepath = u'http://www.dytt8.net'
pagepath = u'http://www.dytt8.net/html/tv/oumeitv/'
vtype = u'tv'
vtag = u'omtv'
logger = logging.getLogger('django')
def main():
	try:
		pagelist = getpagelist()
		print(len(pagelist))
		logger.info(len(pagelist))
		if(len(pagelist)<1):
			logger.error('getpage error ,list < 1')
			return
		dbcount = 0
		try:
			dbcount = models.Video.objects.filter(type=vtype,tag=vtag).count()
		except Exception,e:
			logger.error(e.message)
		logger.info('dbcount is ======================'+str(dbcount))
		#dbcount=0
		endpage = dbcount/25 if dbcount%25 == 0 else dbcount/25 + 1
		lastpage = gettvlist(pagepath+pagelist[-1].get('value'))
		onlinecount = (len(pagelist)-1)*25+len(lastpage)
		logger.info('onlinecount is ======================'+str(onlinecount))
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
						models.FailVideo.objects.save(url=pagepath+pagelist[i].get('value'),type=pagelist)
				except Exception,e:
					continue
		singleSave(gettvlist(pagepath+pagelist[difpage].get('value')))
	except Exception,e:
		logger.error(e.message)
		

def gettvlist(url):
	print('getlist url ============================='+url)
	logger.info('getlist url ============================='+url)
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
	logger.info('gettvlist result length ============='+str(len(tvList)))
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
		logger.info('start batchsave---------------------------------------------------------')
		batchList = []
		for i in range(len(list)):
			surl = basepath + list[i].get('href')
			sname = list[i].string
			if(len(sname)>6):
				batchList.append(models.Video(name=sname.encode('utf-8'),url=surl,type=vtype,tag=vtag))
		models.Video.objects.bulk_create(batchList)
		return True			
	except:
		return False	

# return False or True
def singleSave(list):
	try:
		logger.info('start singlesave---------------------------------------------------------')
		for i in range(len(list)):
			try:
				surl = basepath + list[i].get('href')
				sname = list[i].string
				if(len(sname)>6):
					models.Video.objects.create(name=sname.encode('utf-8'),url=surl,type=vtype,tag=vtag)
			except Exception,e:
				logger.error(e.message)
		return True
	except Exception,e:
		return False

def savevideo(list):
	try:
		batchlist = []
		for i in range(len(list)):
			vname = list[i].string
			vurl = basepath + list[i].get('href')
			#batchlist.append(models.Video(name=vname[0:-1]+']',url=vurl,type='tv',tag='omtv'))
			batchlist.append(models.Video(name=vname.encode('utf-8'),url=vurl,type='tv',tag='omtv'))
		models.Video.objects.bulk_create(batchlist)
	except Exception,e:
		logger.error(e.message)

def startjob():
	try:
		cc = models.Video.objects.all().count()
		logger.info(cc)
	except Exception,e:
		logger.error(e.message)
	#list = gettvlist(u'http://www.dytt8.net/html/tv/oumeitv/list_9_13.html')
	#savevideo(list)
	#list2 = []
	#logger.info('start job')
	#list2.append(models.Video(name=u'2010主打美剧《超感警探 第三季》更新第23-24集[中英双字]',url='/html/tv/oumeitv/20100924/28361.html',type='tv',tag='omtv'))
	#savevideo(list2)

if __name__ == '__main__':
	main()
