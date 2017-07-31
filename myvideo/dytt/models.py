# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Video(models.Model):
	name = models.CharField(max_length=100)
	url = models.CharField(max_length=100)
	picurl = models.CharField(max_length=100)
	description = models.TextField()
	type = models.CharField(max_length=20)
	tag = models.CharField(max_length=20)
	score = models.IntegerField(default=0)
	qrytime = models.IntegerField(default=0)
	parentid = models.IntegerField(default=0)
	childsize = models.IntegerField(default=0)
	class Meta:
		db_table = 'video'
		unique_together =('name','url')
	@classmethod
	def getcount(self, *args, **kwargs):
		try:
			return super(Video,self).objects.filter(*args,**kwargs).count()
		except Exception,e:
			return 0
class FailVideo(models.Model):
	url = models.CharField(max_length=100)
	type = models.CharField(max_length=20)
	class Meta:
		db_table = 'failvideo'
		unique_together =('url','type')
	@classmethod
	def save(self,*args, **kwargs):
		try:
			super(FailVideo,self).save(*args,**kwargs)
		except Exception,e:
			logger.error(e.message)
