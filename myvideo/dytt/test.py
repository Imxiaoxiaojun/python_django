#coding = utf-8
import models
import logging
logger = logging.getLogger('django')
def testjob():
	list = []
	logger.info('start job')
	list.append(models.Video(**{'name':'test1','type':'tv','tag':'omtv','url':'http://www.baidu.com'}))
	list.append(models.Video(**{'name':'test2','type':'tv','tag':'omtv','url':'http://www.baidu.com'}))
	savevideo(list)	
def savevideo(list):
	try:
		models.Video.objects.bulk_create(list)
	except:
		logger.error('save error')
if __name__ == '__main__':
	print('111')
