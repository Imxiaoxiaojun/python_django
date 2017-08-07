from django.conf.urls import url
from django.contrib import admin
from views import *
urlpatterns = [
	url(r'^admin/', admin.site.urls),
    url(r'^getvideos/',main),
	#url(r'^articles/',videoinfo),
	url(r'^articles',videoinfo),
]

