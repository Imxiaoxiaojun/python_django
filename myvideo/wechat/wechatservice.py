# -*- coding: utf-8 -*-
import models
import logging
from news import *
import json
logger = logging.getLogger('django')
basepath = 'http://106.14.165.228/wechat/articles'
def getVideoListByName(val):
	videoList = []
	try:
		list = models.Video.objects.filter(name__contains=val,parentid=0).values('id','type','name','url','picurl','description')	
		for i in range(len(list)):
			#obj = {'title':list[i].get('name'),'url':list[i].get('ur')}
			vurl = basepath + '?id=' + str(list[i].get('id'))
			if str(list[i].get('type'))=='tv':
				vurl += '&type=' + str(list[i].get('type'))
			obj = News(list[i].get('name'),vurl)
			#if(list[i].get('picurl') != ''):
			#	news.picurl(str(list[i].get('picurl')))
			videoList.append(News.class_to_dict(obj))
		#videoList.extend(list)
	except Exception,e:
		logger.error(e.message)
	return videoList

def gettvlist(val):
	tvlist = []
	try:
		tvlist = models.Video.objects.filter(parentid=val).values('name','url')
	except Exception,e:
		logger.error(e.message)
	return tvlist
