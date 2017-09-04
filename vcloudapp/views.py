# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import time
import commands

import re

# import uuid
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from django.utils.timezone import now, timedelta
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
    power = get_power(username)
    return render(request, 'overview.html', context={"power": power})


# 云主机
def instances(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    data = Instances.objects.filter(belonged=username).values()
    # 获取现在的时间与订单期限对比
    now_time = now()
    Filter_Data = Instances.objects.filter(belonged=username).filter(expired_at__lte=now_time)
    if Filter_Data:
        Filter_Data.update(status=2)
    u = []
    for i in data:
        if i['status'] == 0:
            i['status'] = 'running'
        if i['status'] == 1:
            i['status'] = 'stopped'
        if i['status'] == 2:
            i['status'] = 'expire'
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
    limit = 10  # 每页显示的记录数
    paginator = Paginator(u, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'instances.html', context={'power': power, 'instancesData': topics})


# 云盘
def disk(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    return render(request, 'disk.html', context={'power': power})


# 快照
def snapshot(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    return render(request, 'snapshot.html', context={"power": power})


# 日志
def log(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    return render(request, 'log.html', context={"power": power})


# 订单
def order(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    data = Order.objects.filter(created_user=username).values()
    u = []
    for i in data:
        # 判断三级审批
        if (i['dept_pending'] == 0) and (i['admin_pending'] == 0) and (i['vcloud_pending']) == 0:
            i['status'] = 0
        # 0 - 已完成，1 - 审核中，2 - 已过期
        if i['status'] == 0:
            i['status'] = "已完成"
        if i['status'] == 1:
            i['status'] = "审核中"
        if i['status'] == 2:
            i['status'] = "已过期"
        u.append(i)
    limit = 10  # 每页显示的记录数
    paginator = Paginator(u, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'order.html', context={'power': power, 'order': topics})


# 创建实例跳转
def create_instance(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    network = Network.objects.values()
    # print list(network)
    obj = {}
    arr = []
    obj['windows'] = ['win1', 'win2', 'win3']
    obj['linux'] = ['lin1', 'lin2', 'lin3']
    arr.append(obj)
    # print dir(list(arr))
    return render(request, 'create_instance.html', context={'network': list(network), 'data': list(arr)})


# 创建订单
def order_create(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'order_create.html')


# 审核中
def order_checking(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    # 判断是否是管理员权限 防止复制链接进入管理审批界面
    username = request.session.get('username')
    dept = UserInfo.objects.get(username=username).dept
    power = get_power(username)
    if power == 'false':
        return HttpResponseRedirect('/error/')
    u = []
    if power == 'true':
        a = Power.objects.filter(dept_admin='person2').values()
        print list(a)
        # Order.objects.filter(dept=dept).exclude(dept_pending=0)
        data = Order.objects.values()
        for i in data:
            i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
            if i['dept_pending'] == 0:
                i['status'] = "已通过"
            if i['dept_pending'] == 1:
                i['status'] = "审核中"
            if i['status'] == 2:
                i['status'] = "已过期"
            u.append(i)
    limit = 10  # 每页显示的记录数
    paginator = Paginator(u, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'order_checking.html', context={'approval': topics, 'dept': dept})


# 审核中的接口吐数据
@csrf_exempt
def approval(request):
    # 工单号 时间 事由 申请人 状态 操作
    pid = request.POST.get('_id')
    _status = request.POST.get('_status')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    data = ""
    u = []
    if _status == 'y':
        # 同意 继续
        if power == 0:
            return HttpResponseRedirect('/overview/')
        elif power == 1:
            Order.objects.filter(pid=pid).update(dept_pending=0)
            data = Order.objects.exclude(status=2).exclude(dept_pending=0).values()
        elif power == 2:
            Order.objects.filter(pid=pid).update(admin_pending=0)
            data = Order.objects.exclude(status=2).exclude(admin_pending=0).values()
        elif power == 3:
            Order.objects.filter(pid=pid).update(vcloud_pending=0)
            data = Order.objects.exclude(status=2).exclude(vcloud_pending=0).values()
    else:
        # 否定 直接过期
        if power == 0:
            return HttpResponseRedirect('/overview/')
        elif power == 1:
            Order.objects.filter(pid=pid).update(status=2)
            data = Order.objects.exclude(status=2).exclude(dept_pending=0).values()
        elif power == 2:
            Order.objects.filter(pid=pid).update(status=2)
            data = Order.objects.exclude(status=2).exclude(admin_pending=0).values()
        elif power == 3:
            Order.objects.filter(pid=pid).update(status=2)
            data = Order.objects.exclude(status=2).exclude(vcloud_pending=0).values()
    for i in data:
        i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
        if i['dept_pending'] == 0:
            i['status'] = 0
        if i['dept_pending'] == 1:
            i['status'] = 1
        if i['status'] == 0:
            i['status'] = "已通过"
        if i['status'] == 1:
            i['status'] = "审核中"
        if i['status'] == 2:
            i['status'] = "已过期"
        u.append(i)
    return JsonResponse({'data': list(u)})
    # return HttpResponseRedirect('/order_checking/')


# 已完成
def order_finished(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    # 判断是否是管理员权限 防止复制链接进入管理审批界面
    username = request.session.get('username')
    dept = UserInfo.objects.get(username=username).dept
    power = get_power(username)
    if power == 'false':
        return HttpResponseRedirect('/error/')
    u = []
    if power == 0:
        return HttpResponseRedirect('/overview/')
    elif power == "":  # 如果没有权限 返回报错页面
        return HttpResponseRedirect('/error/')
    elif power == 1:
        data = Order.objects.filter(Q(status=2) | Q(dept_pending=0)).filter(dept=dept).values()
        for i in data:
            i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
            if i['dept_pending'] == 0:
                i['status'] = "已通过"
            if i['status'] == 2:
                i['status'] = "拒绝/过期"
            u.append(i)
    elif power == 2:
        data = Order.objects.filter(Q(status=2) | Q(admin_pending=0)).values()
        for i in data:
            i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
            if i['admin_pending'] == 0:
                i['status'] = "已通过"
            if i['status'] == 2:
                i['status'] = "拒绝/过期"
            u.append(i)
    elif power == 3:
        data = Order.objects.filter(Q(status=2) | Q(vcloud_pending=0)).values()
        for i in data:
            i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
            if i['vcloud_pending'] == 0:
                i['status'] = "已通过"
            if i['status'] == 2:
                i['status'] = "拒绝/过期"
            u.append(i)
    limit = 10  # 每页显示的记录数
    paginator = Paginator(u, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'order_finished.html', context={'finish': topics})


def finished(request):
    pid = request.POST.get('_id')
    _status = request.POST.get('_status')
    username = request.session.get('username')
    power = UserInfo.objects.get(username=username).power
    dept = UserInfo.objects.get(username=username).dept
    data = ""
    u = []
    if _status == 'back':
        # 撤销继续
        if power == 0:
            return HttpResponseRedirect('/overview/')
        elif power == 1:
            Order.objects.filter(pid=pid).update(dept_pending=1, status=1)
            data = Order.objects.filter(dept=dept).exclude(dept_pending=1).values()
        elif power == 2:
            Order.objects.filter(pid=pid).update(admin_pending=1, status=1)
            data = Order.objects.exclude(status=2).exclude(admin_pending=1).values()
        elif power == 3:
            Order.objects.filter(pid=pid).update(vcloud_pending=1, status=1)
            data = Order.objects.exclude(status=2).exclude(vcloud_pending=1).values()
    for i in data:
        i['created_at'] = datetime.datetime.strftime(i['created_at'], '%Y-%m-%d %H:%M:%S')
        if i['dept_pending'] == 0:
            i['status'] = "已通过"
        if i['dept_pending'] == 1:
            i['status'] = "审核中"
        if i['status'] == 2:
            i['status'] = "过期"
        u.append(i)
    return JsonResponse({'data': list(u)})


#  注册接口注册完跳login
def userRegister(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    email = request.POST.get('e_mail', None).strip()
    dept = request.POST.get('dept', 'other')
    reg_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    date = time.time()
    reg_time = time.strftime('%Y-%m-%d %X', time.localtime(date))
    # 错误信息
    error = [
        '用户名至少6个字符以上！',
        '用户名必须字母开始！',
        "用户名由字母和数字组成，且必须以字母开头!",
        "密码至少8位及以上，包含大小写字母数字及特殊字符！",
        '用户名已存在',
    ]
    if len(username) < 6:
        return render(request, 'register.html', context={'err_name': error[0]})
    if username[0].isdigit() or not username[0].isalpha():
        return render(request, 'register.html', context={'err_name': error[1]})
    for i in username:
        if not i.isalnum():
            return render(request, 'register.html', context={'err_name': error[2]})
    if len(password) < 8:
        return render(request, 'register.html', context={'err_password': error[3]})
    if UserInfo.objects.filter(username__exact=username):
        return render(request, 'register.html', {'err_name': error[4]})
    md5_password = hashlib.md5(password).hexdigest().upper()
    data = UserInfo(username=username, email=email, password=md5_password, dept=dept, reg_time=reg_time, reg_ip=reg_ip,
                    last_ip=reg_ip)
    data.save()
    return HttpResponseRedirect('/login/')


# 验证登录
def checkLogin(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
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
        date = time.time()
        login_time = time.strftime('%Y-%m-%d %X', time.localtime(date))
        request.session['now_time'] = login_time
        request.session.set_expiry(20000 * 60)
        dept = UserInfo.objects.get(username=username).dept
        power = get_power(username)
        data.save()
        return render(request, 'overview.html', context={"power": power})


# 创建实例接口
# 防止页面403不提交引入 csrf
@csrf_exempt
def chkcreate_instance(request):
    ins_name = request.POST.get('instance_name', None)
    sameName = Instances.objects.filter(name=ins_name)
    # 获取所在部门
    username = request.session.get('username')
    if username:
        dept = UserInfo.objects.get(username=username).dept
    if sameName:
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
    price = request.POST.get('price', 151)
    price = float(price)
    date = time.time()
    apply_time = time.strftime('%Y-%m-%d %X', time.localtime(date))

    date_order = now() + timedelta(days=3)  # 生成订单失效时间
    buy_days = int(expired) * 30
    # print buy_days
    date_expire = now() + timedelta(days=buy_days)
    # print date_expire

    # 选择操作系统
    if os == 'Win2008R2 64':
        os = 1
        cmd_os = 'win2k8r2-v3'
    if os == 'Win2008R2 64(SQLServer)':
        os = 2
    if os == "Win2012R2 64":
        os = 3
    if os == "Win2012R2 64(SQLServer)":
        os = 4
    if os == "CentOS7.2":
        os = 5
        cmd_os = 'centos7-v2'
    if os == "CentOS7.2 + Lamp":
        os = 6
    # 生成操作日志
    log_data = Log(log_type=1, log_opt=apply_time, log_user=username, log_detail="申请云主机", log_ip=ip)
    log_data.save()

    # 生成订单
    uuid_one = str(uuid.uuid4())  # 生成一个关联uuid
    # print uuid_one
    if network == "VLan11":
        network = 'vlan11'
    if network == "VxLan1":
        network = 'vxlan'
    # 处理购买数量 生成对应条数数据
    number = int(buy_number)
    flavor = get_flavor(cpu, mem)

    for i in range(number):
        # 买几个生成几个主机
        ins_data = Instances(create_at=apply_time, expired_at=date_expire, delayed_at=apply_time, belonged=username,
                             name=ins_name, vcpus=cpu, memory=mem, bandwidth=bandwidth, os=os, disk=disk)
        ins_data.save()
        # 生成订单明细
        order_detail = OrderDetail(uuid=uuid_one, vcpu=cpu, memory=mem, bandwidth=bandwidth, os=os, disk=disk,
                                   password=password, expire=expired, network=network, price=price, flavor=flavor)
        order_detail.save()
        # 生成订单
        order_data = Order(created_at=apply_time, created_user=username, expired_at=date_order, uuid=uuid_one,
                           dept=dept)
        order_data.save()
    # 创建虚机命令
    create_virtual(password, flavor, cmd_os, network, ins_name)
    return HttpResponseRedirect('/overview/')


# 获取分配资源
def get_flavor(vcpu, mem):
    flavor = 'Large-01'
    if vcpu == 1 and mem == 1:
        flavor = 'Mini-Linux'
    if vcpu == 1 and mem == 2:
        flavor = 'Small-Linux'
    if vcpu == 1 and mem == 4:
        flavor = 'Small'
    if vcpu == 2 and mem == 2:
        flavor = 'Medium-01'
    if vcpu == 2 and mem == 4:
        flavor = 'Medium-02'
    if vcpu == 4 and mem == 4:
        flavor = 'Large-01'
    if vcpu == 4 and mem == 8:
        flavor = 'Large-02'
    if vcpu == 4 and mem == 16:
        flavor = "Huge-01"
    return flavor


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
# @JSON(format="yyyy-MM-dd HH:mm:ss")
def accessLog(request):
    username = request.session.get('username')
    data = Log.objects.filter(log_user=username).order_by('-log_user', '-log_type', '-log_detail', '-log_ip',
                                                          '-log_opt').values('log_user', 'log_type', 'log_detail',
                                                                             'log_ip', 'log_opt')
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
    print list(u)
    return JsonResponse({'data': list(u)})


# 发送更改密码邮件
@csrf_exempt
def send_email(request):
    username = request.POST.get('username', None)
    check_mail = UserInfo.objects.filter(username__exact=username)
    if check_mail:
        email = UserInfo.objects.get(username=username).email
        try:
            #  第一个是 邮件的标题
            #  第二个是 邮件的内容
            #  第三个是 邮件的发起人账号 管理员邮箱
            #  第四个是 给谁发送可多人
            email_title = '密码重置通知!'
            email_password = "".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8))
            # print email_password
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


# def check_code(request):
#     email = request.POST.get('email')
#     print email
#     return


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


# 获取是否有权限
def get_power(username):
    _username = str(username)
    # data = Power.objects.filter(dept_name=dept).values()
    data = Power.objects.values('dept_admin')
    arr = list(data)
    u = []
    for i in arr:
        a = i['dept_admin'].split(',')
        u.extend(a)
    if _username in u:
        return 'true'
    return 'false'


# 创建虚机的命令
def create_virtual(password, flavor, os_name, net_name, ins_name):
    # Linux
    lin_CMD = 'nova --os-auth-url http://controller01:35357/v3 --os-project-name admin --os-username admin --os-password Centos123 boot --meta password=%s --flavor %s --image %s --nic net-name=%s %s' % (
        password, flavor, os_name, net_name, ins_name)
    (status, output) = commands.getstatusoutput(lin_CMD)
    print output
    if status == 0:
        print "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX success!"
    else:
        print 'OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO failed!'

        # windows
        # win_CMD = 'nova --os-auth-url http://controller01:35357/v3 --os-project-name admin --os-username admin --os-password Centos123 boot --meta admin_pass=%s --flavor %s --image %s --nic net-name=%s %s' % (
        # password, flavor, os_name, net_name, ins_name)
        # print commands.getstatusoutput(win_CMD)


# 身份证号码验证
def check_id_card(idcard):
    Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
            "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    idcard = str(idcard)
    idcard = idcard.strip()
    idcard_list = list(idcard)

    # 地区校验
    area_id = str(idcard[0:2])
    if area_id not in area:
        return 'no pass'

    # 15位身份号码检测
    if len(idcard) == 15:
        if (int(idcard[6:8]) + 1900) % 4 == 0 or ((int(idcard[6:8]) + 1900) % 100 == 0 and (int(idcard[6:8]) + 1900) % 4 == 0):
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
        if (re.match(ereg, idcard)):
            return 'pass'
        else:
            return 'no pass'
    # 18位身份号码检测
    elif len(idcard) == 18:
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if int(idcard[6:10]) % 4 == 0 or (int(idcard[6:10]) % 100 == 0 and int(idcard[6:10]) % 4 == 0):
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # //测试出生日期的合法性
        if re.match(ereg, idcard):
            # //计算校验位
            S = (int(idcard_list[0]) + int(idcard_list[10])) * 7 + (int(idcard_list[1]) + int(idcard_list[11])) * 9 +(int(idcard_list[2]) + int(idcard_list[12])) * 10 + (int(idcard_list[3]) + int(idcard_list[13])) * 5 +(int(idcard_list[4]) + int(idcard_list[14])) * 8 + (int(idcard_list[5]) + int(idcard_list[15])) * 4 + (int(idcard_list[6]) + int(idcard_list[16])) * 2 + int(idcard_list[7]) * 1 + int(idcard_list[8]) * 6 + int(idcard_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if (M == idcard_list[17]):  # 检测ID的校验位
                return 'pass'
            else:
                return 'no pass'
        else:
            return 'no pass'
    else:
        return 'no pass'


# 测试1
def test1(request):
    return HttpResponseRedirect('/test2/')


# 测试2
@csrf_exempt
def test2(request):
    email = request.POST.get('email')
    if email:
        # email = UserInfo.objects.get(username=username).email
        try:
            #  第一个是 邮件的标题
            #  第二个是 邮件的内容
            #  第三个是 邮件的发起人账号 管理员邮箱
            #  第四个是 给谁发送可多人
            email_title = '感谢注册VDIN, 本次验证码详见内容!'
            email_password = "".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8))
            # print email_password
            email_message = '您本次的注册验证码是： ' + email_password + ", 一个小时内有效！"
            email_sendPerson = 'no-reply@vdin.net'
            email_recPerson = email
            send_mail(email_title, email_message, email_sendPerson, [email_recPerson])

            #  新密码存储至数据库
            # data = UserInfo.objects.get(username=username)
            # md5_password = hashlib.md5(email_password).hexdigest().upper()
            # data.password = md5_password
            # data.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse('请确保所有字段都输入并有效')
    # return render(request, 'test1.html', context={'data': email})


# return
