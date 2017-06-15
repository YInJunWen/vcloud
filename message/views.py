# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *

# Create your views here.

# 主页
def index(request):
    return render(request, 'index.html')
# 登录
def login(request):
    # if request.method == 'POST':

    return render(request, 'login.html')
# 注册
def register(request):
    # all_message = UserInfo.objects.all()
    # for message in all_message:
    #      print message.username
    # reg_Obj = UserInfo()
    # reg_Obj.username = "qwe."
    # reg_Obj.password = "a1234567"
    # reg_Obj.email = "877564747@qq.com"
    # reg_Obj.dept = "yjs"
    # reg_Obj.save()
    return render(request, 'register.html')

# 找回密码
# def cb_password(request):
#     return render(request, 'cb_password.html')

# 创建实例
def create_instance(request):
    return render(request, 'create_instance.html')

# 工单提交
def chkcreate_instance(request):
    if request.method == "POST":
        instance_name = request.POST.get('instance_name', None).strip()
        cpu = request.POST.get('cpu', 0)
        mem = request.POST.get('mem', 0)
        disk = request.POST.get('disk', 0)
        bandwidth = request.POST.get('bandwidth', 0)
        os = request.POST.get('os', 0)
        storage = request.POST.get('storage', 0)
        expired = request.POST.get('expired', 0)
        # 对应系统
        if os == 'Win0':
            os = "win2008R2"
        if os == 'Win1':
            os = "win2008R2Sql2008R2"
        if os == "Win2":
            os = "win2012R2"
        if os == "Win3":
            os = "win2012R2Sql2012R2"
        if os == "Cent0":
            os = "Cenots7.2"
        if os == "Cent1":
            os = "Centos7.2_lamp"
        o = Instance_Orders()
        o.instance_name = instance_name
        o.cpu = cpu
        o.mem = mem
        o.disk = disk
        o.bandwidth = bandwidth
        o.os = os
        o.storage = storage
        o.expired = expired
        o.save()

        o = Logs()
        o.log_type = 'instance'
        o.opt_mode = 'create'
        o.opt_user = 'user'
        o.opt_ip = "0.0.0.0"
        o.save()
    return render(request, 'login.html')

# 注册
def regist(request):
    return render(request, 'register.html')

# 检查注册
def check_regist(request):
    # if True:
        return render(request, 'overview.html')


# 测试
def test1(request):
    # if request.method == "POST":
        # value1 = request.POST.get('value1', None)
        # value2 = request.POST.get('value2', None)
        # o = Test1()
        # o.value1 = value1
        # o.value2 = value2
        print '1'
        return render(request, 'test1.html')

