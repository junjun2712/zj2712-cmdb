# -*- coding: utf-8 -*-
#
# --------------------------------------------------------------------------
# views.py
# --------------------------------------------------------------------------
# auther:liutiansi
# Email:liutiansi@gmail.com
# update:2014-05-20
#
# ---------------------------------------------------------------------------
import os
os.environ.update({"DJANGO_SETTINGS_MODULE": "vmx_manager.settings"})
import django
django.setup()
import os, sys,time
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response,redirect
from django.shortcuts import render, HttpResponseRedirect
from django.template import Context
from django.template.loader import get_template
from omaudit.models import ServerHistory
from django.conf import settings
from django.template import RequestContext
from public.views import *
from django.core.paginator import Paginator, InvalidPage, EmptyPage,PageNotAnInteger
from django.utils.log import configure_logging
from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import render, HttpResponseRedirect
from manager.views import _login_check
import datetime,time
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from omaudit.models import ServerHistory
from django.db.models import Q






"""
=事件任务前端加载方法
"""


@_login_check
def omaudit_run(request):
    username = request.COOKIES.get('name', '')
    each_page = 1
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = '请输入关键词'
        return render(request, 'rzsh.html', {'error_msg': error_msg})

    record_list = ServerHistory.objects.filter(Q(history_command__icontains=q) | Q(history_datetime__icontains=q))
    paginator = Paginator(record_list, each_page)
    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1
    try:
        contacts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        contacts = paginator.page(paginator.num_pages)
    return render_to_response('rzsh.html', {'record_list': contacts, 'query': q})




"""
=事件任务pull方法
"""


def omaudit_pull(request):
    if request.method == 'GET':

        if not request.GET.get('history_id', ''):
            return HttpResponse("history_id null")
            #return render(req, 'remote_cmd.html')
        if not request.GET.get('history_ip', ''):
            return HttpResponse("history_ip null")

        if not request.GET.get('history_user', ''):
            return HttpResponse("history_user null")

        if not request.GET.get('history_datetime', ''):
            return HttpResponse("history_datetime null")

        if not request.GET.get('history_command', ''):
            return HttpResponse("history_command null")

        history_id = request.GET['history_id']
        history_ip = request.GET['history_ip']
        history_user = request.GET['history_user']
        history_datetime = request.GET['history_datetime']
        history_command = request.GET['history_command']

        historyobj = ServerHistory(history_id=history_id, \
                                   history_ip=history_ip, \
                                   history_user=history_user, \
                                   history_datetime=history_datetime, \
                                   history_command=history_command)
        try:
            historyobj.save()
        except Exception, e:
            return HttpResponse("入库失败，请与管理员联系！" + str(e))

        Response_result = "OK"
        return HttpResponse(Response_result)

    else:
        return HttpResponse("非法提交！")
