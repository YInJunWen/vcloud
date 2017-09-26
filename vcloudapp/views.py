# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import random
import time
import commands
import re
import redis as redis
# import sys

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Q
from django.utils.timezone import now, timedelta
from .models import *


# 主页
def home(request):
    user_session = request.session.get('username')
    # print user_session
    return render(request, 'index.html', context={'user_session': user_session})


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
    data = Instances.objects.filter(belonged=username, locked=True).values()
    # 获取现在的时间与订单期限对比
    now_time = now()
    filter_data = Instances.objects.filter(belonged=username).filter(expired_at__lte=now_time)
    if filter_data:
        filter_data.update(status=2)
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
        (rx, tx, ip) = get_traffic(i['name'])
        # print rx[0]
        rx = int(rx[0]) / 1024.0
        tx = int(tx[0]) / 1024.0
        if rx < 1024.0:  # k单位
            i['rx'] = '%s %s' % (round(rx, 2), 'Kb')
            i['tx'] = '%s %s' % (round(tx, 2), 'Kb')
        else:
            rx = rx / 1024.0
            tx = tx / 1024.0
            i['rx'] = '%s %s' % (round(rx, 2), 'Mb')
            i['tx'] = '%s %s' % (round(tx, 2), 'Mb')
        # i['rx'] = rx
        # i['tx'] = tx
        i['ip'] = ip[0]
        u.append(i)
    limit = 7  # 每页显示的记录数
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
    data = Log.objects.filter(log_user=username).values()
    u = []
    for i in data:
        i['log_type'] = LogType.objects.get(log_id=i['log_type']).log_name
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
    return render(request, 'log.html', context={"power": power, "log": topics})


# 订单
def order(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    username = request.session.get('username')
    power = get_power(username)
    data = Order.objects.filter(created_user=username).values()
    # print data
    timing = now()
    expired_data = Order.objects.filter(created_user=username, expired_at__lte=timing, dept_pending=1, vcloud_pending=1)
    if expired_data:
        expired_data.update(dept_pending=2, vcloud_pending=2)
    u = []
    for i in data:
        data = OrderDetail.objects.get(pid=i['pid'])
        i['name'] = data.name
        i['vcpu'] = data.vcpu
        i['memory'] = data.memory
        i['bandwidth'] = data.bandwidth
        i['disk'] = data.disk
        if data.os == 1:
            i['os'] = 'Win2008R2_64'
        if data.os == 2:
            i['os'] = 'Win2008R2_64(SQLServer)'
        if data.os == 3:
            i['os'] = 'Win2008R2_64'
        if data.os == 4:
            i['os'] = 'Win2012R2_64(SQLServer)'
        if data.os == 5:
            i['os'] = 'CentOS7.2'
        if data.os == 6:
            i['os'] = 'CentOS7.2 + Lamp'
        if VcloudReason.objects.filter(pid=i['pid']):
            i['vcloud_approval_person'] = VcloudReason.objects.get(pid=i['pid']).approval_person
            i['vcloud_approval_time'] = VcloudReason.objects.get(pid=i['pid']).vcloud_approval_time
            i['vcloud_reason'] = VcloudReason.objects.get(pid=i['pid']).vcloud_reason
        elif DeptReason.objects.filter(pid=i['pid']):
            i['dept_approval_person'] = DeptReason.objects.get(pid=i['pid']).approval_person
            i['dept_approval_time'] = DeptReason.objects.get(pid=i['pid']).dept_approval_time
            i['dept_reason'] = DeptReason.objects.get(pid=i['pid']).dept_reason
        else:
            i['vcloud_reason'] = '待审批'
            i['dept_reason'] = '待审批'
            # 判断三级审批
        if (i['dept_pending'] == 0) and (i['vcloud_pending']) == 0:
            i['status'] = "已通过"
        if (i['dept_pending'] == 2) or (i['vcloud_pending']) == 2:
            i['status'] = "已拒绝"
        if (i['dept_pending'] == 2) and (i['vcloud_pending']) == 2:
            i['status'] = "已过期"
        # 0 - 已完成，1 - 待审核，2 - 已过期
        if i['status'] == 1:
            i['status'] = "待审核"
        u.append(i)
    limit = 7  # 每页显示的记录数
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
    # o = logined(request)
    # if not o:
    #     return HttpResponseRedirect('/login/')
    network = Network.objects.values()
    # obj = {}
    # arr = []
    # # obj['windows'] = ['win1', 'win2', 'win3']
    # # obj['linux'] = ['lin1', 'lin2', 'lin3']
    # arr.append(obj)
    # return render(request, 'create_instance.html', context={'network': list(network), 'data': list(arr)})
    return render(request, 'create_instance.html', context={'network': list(network)})


# 创建订单
def order_create(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    return render(request, 'order_create.html')


# 待审核
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
    dept_arr = dept_list(username)
    u = []
    m = []
    for i in dept_arr:
        if i == 'yjs_center' or i == "zjb":
            a = list(Order.objects.filter(dept_pending=0, vcloud_pending=1).values())
            u.extend(a)
            for j in u:
                if j['vcloud_pending'] == 0:
                    j['status'] = "已通过"
                if j['vcloud_pending'] == 1:
                    j['status'] = "待审核"
                if j['vcloud_pending'] == 2:
                    j['status'] = "已过期"
                # 获取pid
                ins_data = Instances.objects.get(pid=j['pid'])
                j['name'] = OrderDetail.objects.get(pid=j['pid']).name
                # print j['name']
                j['vcpus'] = ins_data.vcpus
                j['memory'] = ins_data.memory
                j['disk'] = ins_data.disk
                j['bandwidth'] = ins_data.bandwidth
                j['dept_admin'] = Power.objects.get(dept_name='yjs').dept_admin
                if ins_data.os == 1:
                    ins_data.os = 'Win2008R2_64'
                if ins_data.os == 2:
                    ins_data.os = 'Win2008R2_64(SQLServer)'
                if ins_data.os == 3:
                    ins_data.os = 'Win2008R2_64'
                if ins_data.os == 4:
                    ins_data.os = 'Win2012R2_64(SQLServer)'
                if ins_data.os == 5:
                    ins_data.os = 'CentOS7.2'
                if ins_data.os == 6:
                    ins_data.os = 'CentOS7.2 + Lamp'
                j['os'] = ins_data.os
                m.append(j)
        else:
            a = list(Order.objects.filter(dept=i, dept_pending=1).exclude(dept_pending=(0 | 2)).values())
            u.extend(a)
            for j in u:
                # print j['dept']
                if j['dept_pending'] == 0:
                    j['status'] = "已通过"
                if j['dept_pending'] == 1:
                    j['status'] = "待审核"
                if j['dept_pending'] == 2:
                    j['status'] = "已过期"
                # 获取pid
                ins_data = Instances.objects.get(pid=j['pid'])
                j['name'] = OrderDetail.objects.get(pid=j['pid']).name
                j['vcpus'] = ins_data.vcpus
                j['memory'] = ins_data.memory
                j['disk'] = ins_data.disk
                j['bandwidth'] = ins_data.bandwidth
                j['dept_admin'] = Power.objects.get(dept_name=j['dept']).dept_admin
                if ins_data.os == 1:
                    ins_data.os = 'Win2008R2_64'
                if ins_data.os == 2:
                    ins_data.os = 'Win2008R2_64(SQLServer)'
                if ins_data.os == 3:
                    ins_data.os = 'Win2008R2_64'
                if ins_data.os == 4:
                    ins_data.os = 'Win2012R2_64(SQLServer)'
                if ins_data.os == 5:
                    ins_data.os = 'CentOS7.2'
                if ins_data.os == 6:
                    ins_data.os = 'CentOS7.2 + Lamp'
                j['os'] = ins_data.os
                m.append(j)
    info_number = len(m)
    limit = 7  # 每页显示的记录数
    paginator = Paginator(m, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'order_checking.html', context={'approval': topics, 'power': power, 'dept': dept, 'info_number': info_number})


# 待审核的接口吐数据
def approval(request):
    username = request.session.get('username')
    reason = request.POST.get('reason')  # 获取用户填写的拒绝理由
    now_time = now()
    # print now_time
    power = get_power(username)
    if not power:
        return HttpResponseRedirect('/error/')
    # 工单号 时间 事由 申请人 状态 操作
    pid = request.POST.get('_id')
    _status = request.POST.get('_status')
    dept_arr = dept_list(username)
    o = ""
    if _status == 'y':
        # 判断此用户权限
        for i in dept_arr:
            if i == 'yjs_center':
                detail_data = OrderDetail.objects.get(pid=pid)  # 获取当前 id 的Object
                os = detail_data.os
                os_name = OS.objects.get(pid=os).os_name  # 获取虚机创建系统名称
                os_type = OS.objects.get(pid=os).os_type  # 获取是linux还是windows
                # 创建虚机命令
                o = create_virtual(detail_data.password, detail_data.flavor, os_name, detail_data.network, detail_data.name, os_type)
                if o == '1':  #
                    data = VcloudReason(pid=pid, vcloud_approval_time=now(), vcloud_reason='同意', approval_person=username)
                    data.save()
                    Order.objects.filter(pid=pid).update(vcloud_pending=0)
                    Instances.objects.filter(pid=pid).update(locked=1)
                    admin_email(pid)
                # else:
                #     JsonResponse({'a': '虚机没搞出来！出错啦！'})
            else:
                Order.objects.filter(pid=pid).update(dept_pending=0)
                data = DeptReason(pid=pid, dept_approval_time=now(), dept_reason='同意', approval_person=username)
                data.save()
    else:
        for i in dept_arr:
            if i == 'yjs_center':
                Order.objects.filter(pid=pid).update(vcloud_pending=2)
                data = VcloudReason(pid=pid, vcloud_approval_time=now(), vcloud_reason=reason, approval_person=username)
                data.save()
            else:
                Order.objects.filter(pid=pid).update(dept_pending=2)
                data = DeptReason(pid=pid, dept_approval_time=now(), dept_reason=reason, approval_person=username)
                data.save()
    #  少了经理级别和云计算经理级别的 拒绝反馈

    info_number(request, username)
    # print o
    return JsonResponse({'a': o})


# 已完成
def order_finished(request):
    o = logined(request)
    if not o:
        return HttpResponseRedirect('/login/')
    # 判断是否是管理员权限 防止复制链接进入管理审批界面
    username = request.session.get('username')
    power = get_power(username)
    dept = UserInfo.objects.get(username=username).dept
    if power == 'false':
        return HttpResponseRedirect('/error/')
    dept_arr =dept_list(username)
    u = []
    m = []
    for i in dept_arr:
        if i == 'yjs_center' or i == 'zjb':
            a = list(Order.objects.filter(Q(vcloud_pending=0) | Q(vcloud_pending=2)).values())
            u.extend(a)
            for j in u:
                data = OrderDetail.objects.get(pid=j['pid'])
                j['name'] = data.name
                j['vcpu'] = data.vcpu
                j['memory'] = data.memory
                j['bandwidth'] = data.bandwidth
                j['disk'] = data.disk
                if data.os == 1:
                    j['os'] = 'Win2008R2_64'
                if data.os == 2:
                    j['os'] = 'Win2008R2_64(SQLServer)'
                if data.os == 3:
                    j['os'] = 'Win2008R2_64'
                if data.os == 4:
                    j['os'] = 'Win2012R2_64(SQLServer)'
                if data.os == 5:
                    j['os'] = 'CentOS7.2'
                if data.os == 6:
                    j['os'] = 'CentOS7.2 + Lamp'
                if VcloudReason.objects.filter(pid=j['pid']):
                    j['approval_person'] = VcloudReason.objects.get(pid=j['pid']).approval_person
                    j['vcloud_approval_time'] = VcloudReason.objects.get(pid=j['pid']).vcloud_approval_time
                    j['vcloud_reason'] = VcloudReason.objects.get(pid=j['pid']).vcloud_reason
                if j['vcloud_pending'] == 0:
                    j['status'] = "已通过"
                if j['vcloud_pending'] == 2:
                    j['status'] = "已拒绝"
                m.append(j)
        else:
            a = list(Order.objects.filter(dept=i).filter(Q(dept_pending=0) | Q(dept_pending=2)).values())
            u.extend(a)
            for j in u:
                data = OrderDetail.objects.get(pid=j['pid'])
                j['name'] = data.name
                j['vcpu'] = data.vcpu
                j['memory'] = data.memory
                j['bandwidth'] = data.bandwidth
                j['disk'] = data.disk
                if data.os == 1:
                    j['os'] = 'Win2008R2_64'
                if data.os == 2:
                    j['os'] = 'Win2008R2_64(SQLServer)'
                if data.os == 3:
                    j['os'] = 'Win2008R2_64'
                if data.os == 4:
                    j['os'] = 'Win2012R2_64(SQLServer)'
                if data.os == 5:
                    j['os'] = 'CentOS7.2'
                if data.os == 6:
                    j['os'] = 'CentOS7.2 + Lamp'
                if DeptReason.objects.filter(pid=j['pid']):
                    j['approval_person'] = DeptReason.objects.get(pid=j['pid']).approval_person
                    j['dept_approval_time'] = DeptReason.objects.get(pid=j['pid']).dept_approval_time
                    j['dept_reason'] = DeptReason.objects.get(pid=j['pid']).dept_reason
                if j['dept_pending'] == 0:
                    j['status'] = "已通过"
                if j['dept_pending'] == 2:
                    j['status'] = "已拒绝"
                m.append(j)
    # info_number = len(m)
    # print info_number
    limit = 7  # 每页显示的记录数
    paginator = Paginator(m, limit)
    page = request.GET.get('page')  # 获取页码
    try:
        topics = paginator.page(page)  # 获取某页对应的记录
    except PageNotAnInteger:  # 如果页码不是个整数
        topics = paginator.page(1)  # 取第一页的记录
    except EmptyPage:  # 如果页码太大，没有相应的记录
        topics = paginator.page(paginator.num_pages)  # 取最后一页的记录
    return render(request, 'order_finished.html', context={'finish': topics, 'power': power, 'dept': dept})


# 审核完成
def finished(request):
    pid = request.POST.get('_id')
    _status = request.POST.get('_status')
    username = request.session.get('username')
    power = get_power(username)
    if power == 'false':
        return HttpResponseRedirect('/error/')
    dept_arr = dept_list(username)
    if _status == 'back':
        for i in dept_arr:
            if i == 'yjs_center':
                VcloudReason.objects.filter(pid=pid).delete()
                Order.objects.filter(pid=pid).update(vcloud_pending=1)
            else:
                # 删除之前的评论
                DeptReason.objects.filter(pid=pid).delete()
                if Order.objects.get(pid=pid).vcloud_pending == True:
                    Order.objects.filter(pid=pid).update(dept_pending=1)
                    return JsonResponse({'status': '1'})
    info_number(request, username)
    return JsonResponse({'status': '0'})


#  注册接口注册完跳login
def userRegister(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    email = request.POST.get('e_mail', None).strip()
    dept = request.POST.get('dept', 'other')
    reg_ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    id_card = request.POST.get('id_card')
    u_phone = request.POST.get('u_phone')
    code = request.POST.get('code')
    date = time.time()
    reg_time = time.strftime('%Y-%m-%d %X', time.localtime(date))
    # 验证身份证账号
    id_card_return = check_id_card(id_card)
    return_phone = check_u_phone(u_phone)

    # 错误信息
    error = [
        '用户名至少6个字符以上！',
        '用户名必须字母开始！',
        "用户名由字母和数字组成，且必须以字母开头!",
        "密码至少8位及以上，包含大小写字母数字及特殊字符！",
        '用户名已存在',
        '您的邮箱验证码不正确',
        '请填写正确的身份证证件号！',
        '请填入正确的手机号！'
    ]
    code_data = CheckCode.objects.get(email=email).code

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
    if code != code_data:
        return render(request, 'register.html', context={'err_name': error[5]})
    if id_card_return == 'no_pass':
        return render(request, 'register.html', context={'err_name': error[6]})
    if return_phone == 'no_pass':
        return render(request, 'register.html', context={'err_name': error[7]})
    md5_password = hashlib.md5(password).hexdigest().upper()
    data = UserInfo(username=username, email=email, password=md5_password, dept=dept, reg_time=reg_time, reg_ip=reg_ip,
                    last_ip=reg_ip, id_card=id_card, u_phone=u_phone)
    CheckCode.objects.filter(email=email).delete()
    data.save()
    return HttpResponseRedirect('/login/')


# 验证登录
def checkLogin(request):
    username = request.POST.get('username', None).strip()
    password = request.POST.get('password', None).strip()
    info_number(request, username)
    nowtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%I:%S")
    ip = request.META.get('REMOTE_ADDR', '0.0.0.0')
    md5_password = hashlib.md5(password).hexdigest().upper()
    loginInfo = UserInfo.objects.filter(username__exact=username, password__exact=md5_password)
    data = Log(log_type=0, log_opt=nowtime, log_user=username, log_ip=ip, log_detail="信息")  # 用户登陆 log记录
    if not loginInfo:
        return render(request, 'login.html', context={'err': '用户名或密码错误!'})
    else:
        lock = UserInfo.objects.get(username=username).locked
        if lock:
            return render(request, 'login.html', context={'err': '该用户已被锁定！'})
        request.session['username'] = username
        date = time.time()
        login_time = time.strftime('%Y-%m-%d %X', time.localtime(date))
        request.session['now_time'] = login_time
        request.session.set_expiry(20 * 60)
        power = get_power(username)
        data.save()
        return render(request, 'overview.html', context={"power": power})


# 创建实例接口
def chkcreate_instance(request):
    o = logined(request)
    if not o:
        return render(request, 'login.html', context={'err': '请先登录后再申请！'})
    ins_name = request.POST.get('instance_name', None)
    sameName = Instances.objects.filter(name=ins_name)
    # 获取所在部门
    username = request.session.get('username')
    network = Network.objects.values()
    if username:
        dept = UserInfo.objects.get(username=username).dept
    if sameName:
        # print list(network)
        return render(request, 'create_instance.html', {'err_name': '此名称已存在', 'network': list(network)})
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

    date_order = now() + timedelta(hours=24)  # 生成订单失效时间
    buy_days = int(expired) * 30
    date_expire = now() + timedelta(days=buy_days)
    # print os
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
                                   password=password, expire=expired, network=network, price=price, flavor=flavor, name=ins_name)
        order_detail.save()
        # 生成订单
        order_data = Order(created_at=apply_time, created_user=username, expired_at=date_order, uuid=uuid_one,
                           dept=dept)
        order_data.save()
    return HttpResponseRedirect('/order/')


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
    return JsonResponse({'data': list(u)})


# 发送更改密码邮件
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


# 邮箱注册验证
def check_code(request):
    email = request.POST.get('email')
    if email:
        try:
            #  第一个是 邮件的标题
            #  第二个是 邮件的内容
            #  第三个是 邮件的发起人账号 管理员邮箱
            #  第四个是 给谁发送可多人
            email_title = '感谢注册VDIN, 本次验证码详见内容!'
            email_code = "".join(random.sample('1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 8))
            email_message = '您本次的注册验证码是： ' + email_code + ", 一个小时内有效！"
            email_sendPerson = 'no-reply@vdin.net'
            email_recPerson = email
            send_mail(email_title, email_message, email_sendPerson, [email_recPerson])

            #  注册邮箱及验证版写入临时数据库
            data = CheckCode(email=email, code=email_code)
            data.save()
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        return render(request, 'register.html')
    else:
        return HttpResponse('请确保所有字段都输入并有效')


# 审批通过后发送邮件通知管理员
def admin_email(_id):
    pc_id = _id  # 主机编号
    try:
        #  第一个是 邮件的标题
        #  第二个是 邮件的内容
        #  第三个是 邮件的发起人账号 管理员邮箱
        #  第四个是 给谁发送可多人
        email_title = 'Vdin新建主机通知!'
        email_message = '本次注册的虚机编号为： ' + pc_id
        email_sendPerson = 'no-reply@vdin.net'
        email_recPerson = '877564747@qq.com'
        send_mail(email_title, email_message, email_sendPerson, [email_recPerson])
    except BadHeaderError:
        return HttpResponse('Invalid header found.')


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


# logout 登出
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
def create_virtual(password, flavor, os_name, net_name, ins_name, os_type):
    lin_CMD = 'nova --os-auth-url http://controller01:35357/v3 --os-project-name admin --os-username admin --os-password Centos123 boot --meta password=%s --flavor %s --image %s --nic net-name=%s %s' % (
        password, flavor, os_name, net_name, ins_name)
    win_CMD = 'nova --os-auth-url http://controller01:35357/v3 --os-project-name admin --os-username admin --os-password Centos123 boot --meta admin_pass=%s --flavor %s --image %s --nic net-name=%s %s' % (
        password, flavor, os_name, net_name, ins_name)
    # print ins_name
    if os_type == 'Linux':
        (status, output) = commands.getstatusoutput(lin_CMD)
    else:
        (status, output) = commands.getstatusoutput(win_CMD)
    if status == 0:
        return '1'
    else:
        return '0'


# 身份证号码验证
def check_id_card(id_card):
    Errors = ['验证通过!', '身份证号码位数不对!', '身份证号码出生日期超出范围或含有非法字符!', '身份证号码校验错误!', '身份证地区非法!']
    area = {"11": "北京", "12": "天津", "13": "河北", "14": "山西", "15": "内蒙古", "21": "辽宁", "22": "吉林", "23": "黑龙江",
            "31": "上海", "32": "江苏", "33": "浙江", "34": "安徽", "35": "福建", "36": "江西", "37": "山东", "41": "河南", "42": "湖北",
            "43": "湖南", "44": "广东", "45": "广西", "46": "海南", "50": "重庆", "51": "四川", "52": "贵州", "53": "云南", "54": "西藏",
            "61": "陕西", "62": "甘肃", "63": "青海", "64": "宁夏", "65": "新疆", "71": "台湾", "81": "香港", "82": "澳门", "91": "国外"}
    id_card = str(id_card)
    id_card = id_card.strip()
    id_card_list = list(id_card)

    # 地区校验
    area_id = str(id_card[0:2])
    if area_id not in area:
        return 'no_pass'

    # 15位身份号码检测
    if len(id_card) == 15:
        if (int(id_card[6:8]) + 1900) % 4 == 0 or ((int(id_card[6:8]) + 1900) % 100 == 0 and (int(id_card[6:8]) + 1900) % 4 == 0):
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}$')  # //测试出生日期的合法性
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}$')  # //测试出生日期的合法性
        if (re.match(ereg, id_card)):
            return 'pass'
        else:
            return 'no_pass'
    # 18位身份号码检测
    elif len(id_card) == 18:
        # 出生日期的合法性检查
        # 闰年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))
        # 平年月日:((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))
        if int(id_card[6:10]) % 4 == 0 or (int(id_card[6:10]) % 100 == 0 and int(id_card[6:10]) % 4 == 0):
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|[1-2][0-9]))[0-9]{3}[0-9Xx]$')  # //闰年出生日期的合法性正则表达式
        else:
            ereg = re.compile(
                '[1-9][0-9]{5}19[0-9]{2}((01|03|05|07|08|10|12)(0[1-9]|[1-2][0-9]|3[0-1])|(04|06|09|11)(0[1-9]|[1-2][0-9]|30)|02(0[1-9]|1[0-9]|2[0-8]))[0-9]{3}[0-9Xx]$')  # //平年出生日期的合法性正则表达式
        # //测试出生日期的合法性
        if re.match(ereg, id_card):
            # //计算校验位
            S = (int(id_card_list[0]) + int(id_card_list[10])) * 7 + (int(id_card_list[1]) + int(id_card_list[11])) * 9 +(int(id_card_list[2]) + int(id_card_list[12])) * 10 + (int(id_card_list[3]) + int(id_card_list[13])) * 5 +(int(id_card_list[4]) + int(id_card_list[14])) * 8 + (int(id_card_list[5]) + int(id_card_list[15])) * 4 + (int(id_card_list[6]) + int(id_card_list[16])) * 2 + int(id_card_list[7]) * 1 + int(id_card_list[8]) * 6 + int(id_card_list[9]) * 3
            Y = S % 11
            M = "F"
            JYM = "10X98765432"
            M = JYM[Y]  # 判断校验位
            if (M == id_card_list[17]):  # 检测ID的校验位
                return 'pass'
            else:
                return 'no_pass'
        else:
            return 'no_pass'
    else:
        return 'no_pass'


# 手机号码验证
def check_u_phone(phone):
    # rep = re.compile('^0\d{2,3}\d{7,8}$|^1[358]\d{9}$|^147\d{8}')
    rep = re.compile("^1[34578][0-9]{9}")
    phone_match = rep.match(phone)
    if phone_match:
        return 'pass'
    else:
        return 'no_pass'


# 返回所在部门列表
def dept_list(username):
    dept = UserInfo.objects.get(username=username).dept
    dept_list = dept.split(',')
    return dept_list


# 获取审批提示数量
def info_number(request, username):
    dept_arr = dept_list(username)
    for i in dept_arr:
        if i == 'yjs_center' or i == "zjb":
            number_data = list(Order.objects.filter(dept_pending=0, vcloud_pending=1).values())
        else:
            number_data = list(Order.objects.filter(dept=i, dept_pending=1).exclude(dept_pending=(0 | 2)).values())
    data = len(number_data)
    request.session['number_data'] = data  # 审批条数
    request.session.set_expiry(20 * 60)


# 获取流量接口
# 参数说明
# hostname:云主机名称 rx:接收总流量 tx:发送总流量 返b字节
def get_traffic(hostname):
    r = redis.StrictRedis(host='10.1.1.203')
    rx = r.hmget(hostname, 'rx')
    tx = r.hmget(hostname, 'tx')
    ip = r.hmget(hostname, 'ip')
    return rx, tx, ip


# 获取权限
def get_privileges():
    cmd = 'nova --os-auth-url http://controller01:35357/v3 --os-project-name admin --os-username admin --os-password Centos123'
    return cmd


# ins_name:实例名称
# status=0表示关机成功
# 关机
def shutdown_instance(ins_name):
    # print ins_name
    cmd = get_privileges()
    cmd = cmd + ' stop ' + ins_name
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        Instances.objects.filter(name=ins_name).update(status=1)
        return 'ok'
    else:
        print 'QQQQQQQQQQQQQQQQQQQQ close    ' + output
        return 'false'


# 重启
def reboot_instance(ins_name):
    cmd = get_privileges()
    cmd = cmd + ' reboot ' + ins_name
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        return 'ok'
    else:
        print 'QQQQQQQQQQQQQQQQQQQQ reboot    ' + output
        return 'false'


# 开机
def start_instance(ins_name):
    cmd = get_privileges()
    cmd = cmd + ' start ' + ins_name
    (status, output) = commands.getstatusoutput(cmd)
    if status == 0:
        Instances.objects.filter(name=ins_name).update(status=0)
        return 'ok'
    else:
        print 'QQQQQQQQQQQQQQQQQQQQ open    ' + output
        return 'false'


# 关机接口
def close_pc(request):
    ins_name = request.POST.get('ins_name')
    print ins_name
    i = shutdown_instance(ins_name)
    if i == 'ok':
        return JsonResponse({'status': '0'})
    return JsonResponse({'status': '1'})


# 开机接口
def open_pc(request):
    ins_name = request.POST.get('ins_name')
    i = start_instance(ins_name)
    if i == 'ok':
        return JsonResponse({'status': '0'})
    return JsonResponse({'status': '1'})


# 重启接口
def reboot_pc(request):
    ins_name = request.POST.get('ins_name')
    i = reboot_instance(ins_name)
    if i == 'ok':
        return JsonResponse({'status': '0'})
    return JsonResponse({'status': '1'})


# 测试1
def test1(request):
    return render(request, 'test1.html')


# 测试2
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
        return HttpResponseRedirect('验证码已发送至所填邮箱！')
    else:
        return HttpResponse('请确保所有字段都输入并有效')
    # return render(request, 'test1.html', context={'data': email})


# return
