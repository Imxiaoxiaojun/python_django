# coding=utf-8
import models
import logging
logger = logging.getLogger('django')
def testjob():
	list = []
	logger.info('start job')
	list.append(models.Video(name=u'2010主打美剧《超感警探 第三季》更新第23-24集[中英双字]',url='/html/tv/oumeitv/20100924/28361.html',type='tv',tag='omtv'))
	savevideo(list)	
def savevideo(list):
	try:
		models.Video.objects.bulk_create(list)
	except:
		logger.error('save error')
if __name__ == '__main__':
	print('111')
