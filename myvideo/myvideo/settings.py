# encoding: utf-8 
"""
Django settings for myvideo project.

Generated by 'django-admin startproject' using Django 1.11.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import logging
import django.utils.log
import logging.handlers

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z7$i$bhv-zty9fs^5)b$#*nd#bp9)v%$(zz2+24fbvhyi666_r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#logger setting
ADMINS = (
('zhuyajun','yajun.zhu@aliyun.com'),
)
  
#非空链接，却发生404错误，发送通知MANAGERS
SEND_BROKEN_LINK_EMAILS = True
MANAGERS = ADMINS
  
#Email设置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST= 'smtp.aliyun.com'#QQ邮箱SMTP服务器(邮箱需要开通SMTP服务)
EMAIL_PORT= 25 #QQ邮箱SMTP服务端口
EMAIL_HOST_USER = 'yajun.zhu@aliyun.com' #我的邮箱帐号
EMAIL_HOST_PASSWORD = 'ak325504' #授权码
EMAIL_SUBJECT_PREFIX = 'querymovie' #为邮件标题的前缀,默认是'[django]'
EMAIL_USE_TLS = True #开启安全链接
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER #设置发件人
  
#logging日志配置
LOGGING = {
 'version': 1,
 'disable_existing_loggers': True,
 'formatters': {#日志格式 
 'standard': {
  'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'} 
 },
 'filters': {#过滤器
 'require_debug_false': {
  '()': 'django.utils.log.RequireDebugFalse',
  }
 },
 'handlers': {#处理器
 'null': {
  'level': 'DEBUG',
  'class': 'logging.NullHandler',
 },
 'mail_admins': {#发送邮件通知管理员
  'level': 'ERROR',
  'class': 'django.utils.log.AdminEmailHandler',
  'filters': ['require_debug_false'],# 仅当 DEBUG = False 时才发送邮件
  'include_html': True,
 },
 'debug': {#记录到日志文件(需要创建对应的目录，否则会出错)
  'level':'DEBUG',
  'class':'logging.handlers.RotatingFileHandler',
  'filename': '/opt/weblog/movis.log',#日志输出文件
  'maxBytes':1024*1024*5,#文件大小 
  'backupCount': 50,#备份份数
  'formatter':'standard',#使用哪种formatters日志格式
 },
 'console':{#输出到控制台
  'level': 'DEBUG',
  'class': 'logging.StreamHandler',
  'formatter': 'standard',
 },
 },
 'loggers': {#logging管理器
 'django': {
  'handlers': ['debug'],
  'level': 'DEBUG',
  'propagate': False
 },
 'django.request': {
  'handlers': ['debug','mail_admins'],
  'level': 'ERROR',
  'propagate': True,
 },
 # 对于不在 ALLOWED_HOSTS 中的请求不发送报错邮件
 'django.security.DisallowedHost': {
  'handlers': ['null'],
  'propagate': False,
 },
 } 
}
ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django_crontab',
	'dytt',
	'cktv',
	'wechat',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myvideo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        #'DIRS': [],
        'DIRS': [BASE_DIR+"/templates/",],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
			'libraries': { # Adding this section should work around the issue.
				'wechatfilters' : 'filters.wechatfilters',
			},
        },
    },
]

WSGI_APPLICATION = 'myvideo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'python',
		'USER': 'python',
		'PASSWORD': 'spdb1234',
		'HOST': '106.15.123.212',
		'PORT': '3306',
		'OPTIONS': {
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
		},
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

CRONJOBS = [
	('06 19 * * *', 'dytt.omtv.startjob','>> /opt/weblog/main.log'),
	('35 23 * * *', 'dytt.omtv.main','>> /opt/weblog/main.log'),
	('38 23 * * *', 'dytt.omtv.startvideojob','>> /opt/weblog/main.log'),
	('19 00 * * *', 'dytt.omtv.startfailvideojob','>> /opt/weblog/main.log'),
]
