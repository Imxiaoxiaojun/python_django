# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import logging
logger = logging.getLogger('django')

# Create your models here.
class Video(models.Model):
	name = models.CharField(max_length=180)
	url = models.CharField(max_length=300)
	picurl = models.CharField(max_length=100)
	description = models.TextField()
	type = models.CharField(max_length=20)
	tag = models.CharField(max_length=20)
	score = models.IntegerField(default=0)
	qrytime = models.IntegerField(default=0)
	parentid = models.IntegerField(default=0)
	childsize = models.IntegerField(default=0)
	isdone = models.IntegerField(default=0)
	class Meta:
		db_table = 'video'
		unique_together =('name','tag')

class FailVideo(models.Model):
	url = models.CharField(max_length=100)
	type = models.CharField(max_length=20)
	parentid = models.IntegerField(default=0)
	childsize = models.IntegerField(default=0)
	class Meta:
		db_table = 'failvideo'
		unique_together =('url','type')
