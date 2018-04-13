#coding=utf-8
from django.conf.urls import url
from omaudit.views import *


urlpatterns = [

    url(r'^omaudit_run/(\d+)/$', omaudit_run, name='omaudit_run'),

]