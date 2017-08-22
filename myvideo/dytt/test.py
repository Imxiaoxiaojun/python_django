# -*- coding: UTF-8 -*-
from DBUtil import Mysql
#import models
#import logging
#logger = logging.getLogger('django')
#def testjob():
#	list = []
#	logger.info('start job')
#	list.append(models.Video(name=u'2010主打美剧《超感警探 第三季》更新第23-24集[中英双字]',url='/html/tv/oumeitv/20100924/28361.html',type='tv',tag='omtv'))
#	savevideo(list)	
#def savevideo(list):
#	try:
#		#models.Video.objects.bulk_create(list)
#	except:
#		logger.error('save error')

if __name__ == '__main__':
	conn = Mysql()
	limitNum = 0
	preList = []
	count = limitNum * 1000
	sql = "SELECT listurl FROM  python_prelist ORDER by listid LIMIT 1,20 "
	videos = conn.getAll(sql)
	if videos:
		preList.extend(videos)
	while True:
		for url in preList:
			print url.get('listurl')
		break
