# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response

from django.http.response import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
 
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import (TextMessage, VoiceMessage, ImageMessage,VideoMessage, LinkMessage, LocationMessage, EventMessage)
import logging
from wechatservice import * 
logger = logging.getLogger('django')

wechat_instance = WechatBasic(
	token='johnsmovie',
	appid='wx8df05882fae81331',
	appsecret='7af8c6cbeb2b24e3ea5bcc92134a8476'
)

@csrf_exempt
def videoinfo(request):
	if request.method == 'GET':
		content = {}
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		if not request.GET.get('nsukey'):
			content['errmsg']='请通过公众号访问'
			return render_to_response('wechat/503.html',content)	
		#response = wechat_instance.response_text(content=apply_text)
		if not request.GET.get('id') or request.GET.get('id')=='':
			content['errmsg']='搜索的视频错误'
		if request.GET.get('type') and request.GET.get('type')=='video':
			logger.info('type is video')
		elif request.GET.get('type') and request.GET.get('type')=='tv':
			logger.info(request.GET.get('type'))
			list = gettvlist(request.GET.get('id'))
			content['tvlist'] = list
			return render_to_response('wechat/tvlist.html',content)
		return render_to_response('wechat/503.html',content)
		#return HttpResponse(apply_text, content_type="html")
	
	
@csrf_exempt
def main(request):
	welcome = '欢迎订阅约翰家的杂货铺\n回复"#"+"电视剧/电影名称"搜索视频资源\n例如:"#冰与火"'
	helpmsg = '回复"#"+电视剧/电影名称”搜索视频资源\n例如："#冰与火"'
	tipmsg = '非常抱歉，暂不支持您的指令\n回复help查看更多指令'
	if request.method == "GET":
		signature = request.GET.get('signature')
		timestamp = request.GET.get('timestamp')
		nonce = request.GET.get('nonce')

		if not wechat_instance.check_signature(signature=signature, timestamp=timestamp, nonce=nonce):
			return HttpResponseBadRequest('Verify Failed')

		return HttpResponse(request.GET.get('echostr', ''), content_type="text/plain")

	try:
		wechat_instance.parse_data(data=request.body)
	except ParseError:
		return HttpResponseBadRequest('Invalid XML Data')	
	message = wechat_instance.get_message()		
	apply_text = ''
	response = None
	if isinstance(message, TextMessage):
		content = message.content.strip()
		logger.info(content)
		if (content == 'help'):
			apply_text = helpmsg
		elif(content.startswith('#')):
			list = getVideoListByName(content[1:])
			if(len(list)>0):
				for i in range(len(list)):
					logger.info(list[i])
					logger.info(list[i])
				response = wechat_instance.response_news(list)	
				#return render_to_response('wechat/videolist.xml')
				return HttpResponse(response, content_type="application/xml")
			else:
				apply_text = content
		else:
			apply_text = tipmsg
	response = wechat_instance.response_text(content=apply_text)
	return HttpResponse(response, content_type="application/xml")
