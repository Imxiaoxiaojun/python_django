# coding=utf-8 
import urllib2
import logging
import re
import models
from bs4 import BeautifulSoup
import base64
global basepath,pagepath,vtype,vtag,logger
indexurl = u'http://www.dytt8.net/html/tv/oumeitv/index.html'
basepath = u'http://www.dytt8.net'
pagepath = u'http://www.dytt8.net/html/tv/oumeitv/'
vtype = 'tv'
vtag = 'omtv'
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
					if not(batchSave(list,0)):
						print('batchsave is False')
						models.FailVideo.objects.create(url=pagepath+pagelist[i].get('value'),type='getpagelist')
				except Exception,e:
					logger.error(e.message)
		singleSavetv(gettvlist(pagepath+pagelist[difpage].get('value')),0)
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

def getFailVideoList():
	list = []
	try:
		list.extend(models.FailVideo.objects.all().values('id','url','parentid','childsize','type'))
	except Exception,e:
		logger.error(e.message)
	return list

def startfailvideojob():
	try:
		failvideolist = getFailVideoList()
		if(len(failvideolist)<0):
			return
		for i in range(len(failvideolist)):
			try:
				vurl = failvideolist[i].get('url')
				vparentid = failvideolist[i].get('parentid')
				vid = failvideolist[i].get('id')
				vtype = failvideolist[i].get('type')
				vchildsize = failvideolist[i].get('childsize')
				list = []
				if(vtype == 'getvideolist'):
					list = getvideolist(vurl,vchildsize)
				if(len(list)==vchildsize):
					continue
				if (batchSave(list[1:],vparentid)):
					models.Video.objects.filter(id=vparentid).update(picurl=list[0].get('picurl'),childsize=len(list)-1)
					models.FailVideo.objects.filter(id=vid).delete()
			except Exception,e:
				logger.error(e.message)
	except Exception,e:
		logger.error(e.message)

def startvideojob():
	try:
		parentlist = getParentList()
		if(len(parentlist)<1):
			return
		for i in range(len(parentlist)):
			try:
				vurl = parentlist[i].get('url')
				vchildsize = parentlist[i].get('childsize')
				list = getvideolist(vurl,vchildsize)	
				if(len(list)-1==vchildsize):
					continue

				if not (batchSave(list[1:],parentlist[i].get('id'))):
					#记录日志
					models.FailVideo.objects.create(url=vurl,type='getvideolist',parentid=parentlist[i].get('id'),childsize=vchildsize)
				else:
					models.Video.objects.filter(id=parentlist[i].get('id')).update(picurl=list[0].get('picurl'),childsize=len(list)-1)
			except Exception,e:
				logger.error(e.message)
	except Exception,e:
		logger.error(e.message)


def getvideolist(url,childsize):		
	print('getvideolist  url ============================='+url)
	logger.info('getlist url ============================='+url)
	videos = []
	try:
		rep = urllib2.urlopen(urllib2.Request(url))
		if(rep.code!=200):
			print('html rep code error')
			logger.error('html rep code error')
		html = rep.read().decode('gbk','ignore')
		soup = BeautifulSoup(html,'lxml')
		list = soup.find_all('a',href=re.compile('ftp://(.*)'))
		tvinfo = soup.find_all('p')
		picurl = '' 
		if(childsize<1):
			for i in range(len(tvinfo)):
				try:
					picurl += tvinfo[i].contents[0].get('src')
					break
				except:
					continue
		videos.extend([{'picurl':picurl}])
		videos.extend(list)
	except Exception, e:
		print(e.message)
		logger.error(e.message)
	print('gettvlist result length ============='+str(len(videos)))
	logger.info('gettvlist result length ============='+str(len(videos)))
	return videos

def getParentList():
	parentList = []
	try:
		parentList.extend(models.Video.objects.filter(tag=vtag,parentid=0,isdone=0).values('id','url','childsize'))
		for i in range(len(parentList)):
			logger.info(parentList[i]['url'])
	except Exception,e:
		logger.error(e.message)
	return parentList

def getthunderlink(url):
	try:
		tempurl = ('AA' + url + 'ZZ').encode('utf-8')
		thunderlink = 'thunder://'+base64.b64encode(tempurl)
		#thunderlink = 'thunder://'.encode('utf-8')+base64.b64encode(tempurl)
		return thunderlink.encode('utf-8')
	except Exception,e:
		logger.error(e.message)
		return url.encode('utf-8')

# return False or True
def batchSave(list,parentId):
	try:
		logger.info('start batchsave---------------------------------------------------------')
		batchList = []
		for i in range(len(list)):
			surl = basepath + list[i].get('href') if parentId == 0 else getthunderlink(list[i].get('href'))
			sname = list[i].string
			logger.info(len(surl))
			if(len(sname)>6):
				batchList.append(models.Video(name=sname.encode('utf-8'),url=surl,type=vtype,tag=vtag,parentid=parentId))
				#batchList.append(models.Video(name=sname.encode('utf-8'),url=surl,type=vtype,tag=vtag,parentid=parentId))
		printbatchlist(batchList)
		models.Video.objects.bulk_create(batchList)
		return True			
	except:
		return False	

def printbatchlist(list):
	for i in range(len(list)):
		logger.info(list[i].url)

# return False or True
def singleSavetv(list,parentId):
	try:
		logger.info('start singlesave---------------------------------------------------------')
		for i in range(len(list)):
			try:
				surl = basepath + list[i].get('href') if parentId == 0 else getthunderlink(list[i].get('href'))
				sname = list[i].string
				if(len(sname)>6):
					models.Video.objects.create(name=sname.encode('utf-8'),url=surl,type=vtype,tag=vtag,parentid=parentId)
			except Exception,e:
				logger.error(e.message)
		return True
	except Exception,e:
		return False

def savetv(list):
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

def printlist(list):
	for i in range(len(list)):
		print(getthunderlink(list[i].get('href')))
	

if __name__ == '__main__':
	#main()
	url = u'http://www.dytt8.net/html/tv/oumeitv/20170717/54532.html'
	list = getvideolist(url,0)
	print(list[0].get('picurl'))
	print(getthunderlink(''))
	printlist(list[1:])
