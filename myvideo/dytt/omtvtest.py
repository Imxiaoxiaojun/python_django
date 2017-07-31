#coding=utf-8 
import urllib2
import logging
#import models
class omtv():
	global basepath,indexurl,vtype,vtag
	basepath = 'http://www.baidu.com'
	indexurl = ''
	vtype = ''
	vtag = ''
	logger = logging.getLogger('django')
	def gethtml():
		return False

	def getTvList():
		return False



	# return False or True
	def batchSave(list):
		try:
			models.Video.objects.bluk_create(list)
		except Exception, e:
			logger.error(e.message)
			return False	
		return True			

	# return False or True
	def save(list):
		try:
			1/0
		except Exception, e:
			return False
		return True
	def test():
		print(basepath)
		print(indexurl)
		print(vtype)
		print(vtag)
		#basepath = 'wwwww'
		#print(basepath)
	if __name__ == '__main__':
		test()
