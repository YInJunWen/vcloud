# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import time
import uuid
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from .models import *


# 主页
def home(request):
    return render(request, 'index.html')


#  user登录跳转
def userLogin(request):
    return render(request, 'login.html')


#  注册跳转页面
def register(request):
    return render(request, 'register.html')


# 忘记密码跳转
def get_password(request):
    return render(request, 'repassword.html')


# 中德感知
def zdgz(request):
    return render(request, 'zdgz.html')


# overview
def overview(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'overview.html', context={"power": power})


# 云主机
def instances(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'instances.html', context={'power': power})


# 云盘
def disk(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'disk.html', context={'power': power})


# 快照
def snapshot(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'snapshot.html', context={"power": power})


# 日志
def log(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'log.html', context={"power": power})


# 订单
def order(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    return render(request, 'order.html', context={'power': power})


# 创建实例跳转
def create_instance(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    network = Network.objects.values()
    os = OS.objects.all()
    # print os
    for obj in os:
        print obj.os_type
    return render(request, 'create_instance.html', context={'network': list(network)})


# 创建订单
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


#  注册接口注册完跳login
def userRegister(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    email = request.POST.get('e_mail', None).strip()
    dept = request.POST.get('dept', None).strip()
    reg_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
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
    md5_password = hashlib.md5(password).hexdigest().upper()
    data = UserInfo(username=username, email=email, password=md5_password, dept=dept, reg_time=reg_time, reg_ip=reg_ip,
                    last_ip=reg_ip)
    data.save()
    return HttpResponseRedirect('/login/')


def checkLogin(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    date = time.time()
    nowtime = time.strftime('%Y-%m-%d %X', time.localtime(date))
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    md5_password = hashlib.md5(password).hexdigest().upper()
    loginInfo = UserInfo.objects.filter(username__exact=username, password__exact=md5_password)
    lock = UserInfo.objects.get(username=username).locked
    # print lock
    data = Log(log_type=0, log_opt=nowtime, log_user=username, log_ip=ip, log_detail="信息")  # 用户登陆 log记录
    if lock:
        return render(request, 'login.html', context={'err': '该用户已被锁定！'})
    if not loginInfo:
        return render(request, 'login.html', context={'err': '用户名或密码错误!'})
    else:
        request.session['username'] = username
        request.session.set_expiry(20000 * 60)
        power = UserInfo.objects.get(username=username).power
        data.save()
        return render(request, 'overview.html', context={"power": power})


# 创建实例接口
# 防止页面403不提交引入 csrf
@csrf_exempt
def chkcreate_instance(request):
    ins_name = request.POST.get('instance_name', None)
    sameName = Instances.objects.filter(name=ins_name)
    username = request.session.get('username')
    # print username
    # 获取所在部门
    # username = request.session.get('username')
    # if username:
    #     dept = UserInfo.objects.get(username=username).dept
    # print dept
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
    buy_number = request.POST.get('buy_number', 1)
    password = request.POST.get('password')  # 密码存在订单明细里面
    network = request.POST.get('network')
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    date = time.time()
    apply_time = time.strftime('%Y-%m-%d %X', time.localtime(date))

    # 选择操作系统
    if os == 'Win2008R2 64':
        os = 0
    if os == 'Win2008R2 64(SQLServer)':
        os = 1
    if os == "Win2012R2 64":
        os = 2
    if os == "Win2012R2 64(SQLServer)":
        os = 3
    if os == "CentOS7.2":
        os = 4
    if os == "CentOS7.2 + Lamp":
        os = 5
    # 生成操作日志
    log_data = Log(log_type=1, log_opt=apply_time, log_user=username, log_detail="申请云主机", log_ip=ip)
    log_data.save()

    # 生成订单
    uuid_one = str(uuid.uuid4())  # 生成一个关联uuid
    # print uuid_one
    if network == "华东高防2区":
        network = 1
    if network == "华东高防2双线":
        network = 2
    if network == "广东高速高防":
        network = 3
    if network == "广东高防双线":
        network = 4
    if network == "华南高防2区":
        network = 5
    if network == "华南高防2双线":
        network = 6
    # 处理购买数量 生成对应条数数据
    number = int(buy_number)
    for i in range(number):
        # 买几个生成几个主机
        ins_data = Instances(create_at=apply_time, expired_at=apply_time, delayed_at=apply_time, belonged=username,
                             name=ins_name, vcpus=cpu, memory=mem, bandwidth=bandwidth, os=os, disk=disk)
        ins_data.save()
        # 生成订单明细
        order_detail = OrderDetail(uuid=uuid_one, vcpu=cpu, memory=mem, bandwidth=bandwidth, os=os, disk=disk,
                                   password=password, expire=expired, network=network)
        order_detail.save()
        # 生成订单
        order_data = Order(created_at=apply_time, created_user=username, expired_at=apply_time, uuid=uuid_one)
        order_data.save()
    return HttpResponseRedirect('/overview/')


# 请求价格接口
@csrf_exempt
def calculatePrice(request):
    cpu = str(request.POST.get('cpu', '2'))
    _cpu = int(cpu)
    mem = str(request.POST.get('mem', '4'))
    _mem = int(mem)
    flux = str(request.POST.get('flux', '1'))
    _flux = int(flux)
    disk = str(request.POST.get('disk', '50'))
    _disk = int(disk)
    expired = str(request.POST.get('expired', '1'))
    _expired = int(expired)
    buy_number = str(request.POST.get('buyNumber', '1'))
    _buy_number = int(buy_number)
    price = round((_cpu * 28 + _mem * 15 + _flux * 10 + _disk * 0.5) * _expired * _buy_number, 2)
    return JsonResponse({'price': price})


# 获取日志信息
@csrf_exempt
def accessLog(request):
    username = request.session.get('username')
    data = Log.objects.filter(log_user=username).order_by('-log_user', '-log_type', '-log_detail', '-log_ip',
                                                          '-log_opt').values('log_user', 'log_type', 'log_detail',
                                                                             'log_ip', 'log_opt')
    # print data
    u = []
    for i in data:
        if i['log_type'] == 0:
            i['log_type'] = "登陆"
        if i['log_type'] == 1:
            i['log_type'] = "实例"
        if i['log_type'] == 2:
            i['log_type'] = "磁盘"
        if i['log_type'] == 3:
            i['log_type'] = "快照"
        if i['log_type'] == 4:
            i['log_type'] = "系统"
        u.append(i)
    return JsonResponse({'data': list(u)})


# 获取订单信息
@csrf_exempt
def accessIns(request):
    username = request.session.get('username')
    data = Instances.objects.filter(belonged=username).values()
    # print data
    u = []
    for i in data:
        if i['status'] == 0:
            i['status'] = 'running'
        if i['status'] == 1:
            i['status'] = 'stopped'
        if i['os'] == 0:
            i['os'] = 'Win2008R2_64'
        if i['os'] == 1:
            i['os'] = 'Win2008R2_64(SQLServer)'
        if i['os'] == 2:
            i['os'] = 'Win2008R2_64'
        if i['os'] == 3:
            i['os'] = 'Win2012R2_64(SQLServer)'
        if i['os'] == 4:
            i['os'] = 'CentOS7.2'
        if i['os'] == 5:
            i['os'] = 'CentOS7.2 + Lamp'
        u.append(i)
    print u
    return JsonResponse({'data': list(u)})


# 获取order 订单
@csrf_exempt
def accessOrder(request):
    username = request.session.get('username')
    data = Order.objects.filter(created_user=username).values()
    u = []
    for i in data:
        # 0 - 已完成，1 - 审核中，2 - 已过期
        if i['status'] == 0:
            i['status'] = "已完成"
        if i['status'] == 1:
            i['status'] = "审核中"
        if i['status'] == 2:
            i['status'] = "已过期"
        u.append(i)
    return JsonResponse({'data': list(u)})


# 发送邮件
@csrf_exempt
def send_email(request):
    username = request.POST.get('username', None)
    # from_email = request.POST.get('from_email', None)
    check_mail = UserInfo.objects.filter(username__exact=username)
    print check_mail
    if check_mail:
        email = UserInfo.objects.get(username=username).email
        try:
            #  第一个是 邮件的标题
            #  第二个是 邮件的内容
            #  第三个是 邮件的发起人账号 管理员邮箱
            #  第四个是 给谁发送可多人
            email_title = '密码重置通知!'
            email_password = "".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8))
            print email_password
            email_message = '您的密码已初始化为： ' + email_password + ", 可登录后在控制台页面修改新密码！"
            email_sendPerson = 'no-reply@vdin.net'
            email_recPerson = email
            send_mail(email_title, email_message, email_sendPerson, [email_recPerson])

            #  新密码存储至数据库
            data = UserInfo.objects.get(username=username)
            md5_password = hashlib.md5(email_password).hexdigest().upper()
            data.password = md5_password
            data.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('请确保所有字段都输入并有效')


@csrf_exempt
def change_psw(request):
    username = request.session.get('username')
    old = request.POST.get('old_psw')
    new = request.POST.get('new_psw')
    confirm = request.POST.get('confirm_psw')
    md5_old = hashlib.md5(old).hexdigest().upper()
    SQLpassword = UserInfo.objects.get(username=username).password
    if new == confirm and md5_old == SQLpassword:
        check_old = UserInfo.objects.filter(username__exact=username)
        if check_old:
            md5_new = hashlib.md5(new).hexdigest().upper()
            data = UserInfo.objects.get(username=username)  # 获取这条数据
            data.password = md5_new
            data.save()
            del request.session['username']
            return JsonResponse({'data': '1'})
    else:
        return JsonResponse({'data': '0'})


# 判断是否登录
def logined(request):
    username = request.session.get('username')
    if username:
        return True
    return False


# logout
def logout(request):
    del request.session['username']
    return HttpResponseRedirect('/login/')


# 测试
def test1(request):
    username = request.session.get('username')
    a = UserInfo.objects.get(username=username).power
    return render(request, 'test1.html', context={'a': a})


@csrf_exempt
def test2(request):
    value = request.session.get('username', default=None)
    return JsonResponse({'data': value})
