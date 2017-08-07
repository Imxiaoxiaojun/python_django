#coding:utf-8
from django import template
register = template.Library()


@register.filter
def subvideoname(value):
	index = value.find('www.dy2018.net]')
	if(index == -1):
		return value
	else:
		return value[index+15:]
@register.filter
def formatvideourl(value):
	count = len(value)/50
	url = ''
	index = 0
	for i in range(1,count+1):
		url += value[index:i*50] + '<br>'
		index +=50
	return url 
