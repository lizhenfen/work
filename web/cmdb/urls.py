from __future__ import  absolute_import
from django.conf.urls import url
from . import  views
app_name = 'cmdb'
urlpatterns = [
    url(r'^$', views.home),
    url(r'^servers/$', views.servers, name='servers'),
]
