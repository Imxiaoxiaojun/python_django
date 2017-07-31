#coding = utf-8
import models
import logging
logger = logging.getLogger('django')
def testjob():
	getobj()	
def savevideo(list):
	try:
		list = []
		logger.info('start job')
		list.append(models.Video(**{'name':'test3','type':'tv','tag':'omtv','url':'http://www.baidu.com'}))
		list.append(models.Video(**{'name':'test4','type':'tv','tag':'omtv','url':'http://www.baidu.com'}))
		models.Video.objects.bulk_create(list)
	except:
		logger.error('save error')
def getobj():
	try:
		video = models.Video.objects.get(name='test1')
		logger.info(video.url)
		1/0
	except Exception,e:
		logger.error(e.message)
