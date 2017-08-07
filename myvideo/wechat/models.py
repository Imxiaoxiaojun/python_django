# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from dytt.models import Video

# Create your models here.
class WeChatUser(models.Model):
	username = models.CharField(max_length=100)
	tokenid = models.CharField(max_length=100)
	sex = models.IntegerField(default=2)#0-男,1-女,2-未知
	country = models.CharField(max_length=20)
	isfollow = models.BooleanField(default=False)
	lastlogintime = models.DateField(auto_now =True)
	createtime = models.DateField(auto_now_add=True)
	class Meta:
		db_table = 'wechatuser'
	
