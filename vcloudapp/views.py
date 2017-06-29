# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import time
# from datetime import date

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


# Create your views here.

# 主页
def home(request):
    return render(request, 'index.html')


#  user登录跳转
def userLogin(request):
    return render(request, 'login.html')


#  注册跳转页面
def register(request):
    return render(request, 'register.html')


#  注册接口注册完跳login
def userRegister(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    email = request.POST.get('e_mail', None).strip()
    dept = request.POST.get('dept', None).strip()
    date = time.time()
    reg_time = time.strftime('%Y-%m-%d %X', time.localtime(date))
    if len(username) < 6:
        err_name = '用户名至少6个字符以上！'
        return render(request, 'register.html', context={'err_name': err_name})
    if username[0].isdigit() or not username[0].isalpha():
        err_name = '用户名必须字母开始！'
        return render(request, 'register.html', context={'err_name': err_name})
    for i in username:
        if not i.isalnum():
            err_name = "用户名由字母和数字组成，且必须以字母开头!"
            return render(request, 'register.html', context={'err_name': err_name})
    if len(password) < 8:
        err_name = "密码至少8位及以上，包含大小写字母数字及特殊字符！"
        return render(request, 'register.html', context={'err_password': err_name})
    if UserInfo.objects.filter(username__exact=username):
        err_name = '用户名已存在'
        return render(request, 'register.html', {'err_name': err_name})
    data = UserInfo(username=username, email=email, password=password, dept=dept, reg_time=reg_time)
    data.save()
    return HttpResponseRedirect('/login/')


def checkLogin(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    date = time.time()
    nowtime = time.strftime('%Y-%m-%d %X', time.localtime(date))
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    loginInfo = UserInfo.objects.filter(username__exact=username, password__exact=password)

    # 用户登陆 log记录
    data = UserLog(username=username, actionObject='登录', operationType='信息', ip=ip, logintime=nowtime)
    if not loginInfo:
        return render(request, 'login.html', context={'err': '用户名或密码错误!'})
    else:
        request.session['username'] = username
        request.session.set_expiry(20 * 60)
        data.save()
        return HttpResponseRedirect('/overview/')


# 忘记密码跳转
def get_password(request):
    return render(request, 'repassword.html')


# overview
def overview(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'overview.html')


# 云主机
def instances(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('//')
    return render(request, 'instances.html')


# 云盘
def disk(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'disk.html')


# 快照
def snapshot(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'snapshot.html')


# 日志
def log(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'log.html')


# 工单
def order(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'order.html')


# 创建实例跳转
def create_instance(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'create_instance.html')


# 中德感知
def zdgz(request):
    return render(request, 'zdgz.html')


# 创建工单
def order_create(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'order_create.html')


# 审核中
def order_checking(request):
    return render(request, 'order_checking.html')


# 已完成
def order_finished(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'order_finished.html')


# 创建实例接口
# 防止页面403不提交引入 csrf
@csrf_exempt
def chkcreate_instance(request):
    ins_name = request.POST.get('instance_name', None)
    sameName = instance_Orders.objects.filter(instance_name=ins_name)
    print sameName
    if sameName:
        # print '123'
        return render(request, 'create_instance.html', {'err_name': '此名称已存在'})
    cpu = request.POST.get('cpu', 2)
    mem = request.POST.get('mem', 4)
    disk = request.POST.get('disk', 50)
    bandwidth = request.POST.get('bandwidth', 1)
    os = request.POST.get('os', None)
    storage = request.POST.get('storage', 'sas')
    expired = request.POST.get('expired', 1)
    buyNumber = request.POST.get('buyNumber', 1)
    created_user = request.session.get('username')
    # nowtime = time.strftime('%Y-%m-%d %X', time.localtime(date))
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')

    # 选择操作系统
    if os == 'Win2008R2 64(纯净版)':
        os = "win2008R2"
    if os == 'Win2008R2 64(SQLServer)':
        os = "win2008R2Sql2008R2"
    if os == "Win2012R2 64(纯净版)":
        os = "win2012R2"
    if os == "Win2012R2 64(SQLServer)":
        os = "win2012R2Sql2012R2"
    if os == "CentOS7.2纯净版":
        os = "Cenots7.2"
    if os == "CentOS7.2纯净版 + Lamp":
        os = "Centos7.2_lamp"
    # 生成操作日志
    log_data = UserLog(username=created_user, actionObject='购买', operationType='申请云主机', ip=ip)
    log_data.save()
    # 生成订单
    ins_data = instance_Orders(instance_name=ins_name, mem=mem, cpu=cpu, disk=disk, bandwidth=bandwidth, os=os,
                               storage=storage, expired=expired, buyNumber=buyNumber, created_user=created_user)
    ins_data.save()
    return HttpResponseRedirect('/overview/')


# 请求价格接口
@csrf_exempt
def calculatePrice(request):
    cpu = int(request.POST.get('cpu'))
    mem = int(request.POST.get('mem'))
    flux = int(request.POST.get('flux'))
    disk = int(request.POST.get('disk'))
    expired = int(request.POST.get('expired'))
    buyNumber = int(request.POST.get('buyNumber'))
    price = round((cpu * 28 + mem * 15 + flux * 10 + disk * 0.5) * expired * buyNumber, 2)
    return JsonResponse({'price': price})


# logout
def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')


# 获取日志信息
@csrf_exempt
def accessLog(request):
    username = request.session.get('username')
    data = UserLog.objects.filter(username=username).values('actionObject', 'id', 'ip', 'logintime', 'operationType',
                                                            'username')
    return JsonResponse({'data': list(data)})


@csrf_exempt
def accessIns(request):
    username = request.session.get('username')
    data = instance_Orders.objects.filter(created_user=username).values('bandwidth', 'buyNumber', 'cpu', 'created_user',
                                                                        'disk', 'expired', 'id', 'instance_name', 'mem',
                                                                        'os', 'storage')
    return JsonResponse({'data': list(data)})


# 判断是否登录
def logined(request):
    username = request.session.get('username')
    if username:
        return True
    return False


# 测试
def test1(request):
    return render(request, 'test1.html')


@csrf_exempt
def test2(request):
    value = request.session.get('username', default=None)
    return JsonResponse({'data': value})
