# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

import datetime
from django.db import models
from django.db import connection, transaction

# Create your models here.


# 注册信息表
class UserInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name=u"用户名", primary_key=True)
    password = models.CharField(max_length=32, verbose_name=u"密码")
    email = models.EmailField(verbose_name=u"邮箱")
    dept = models.CharField(max_length=4, default='cp', verbose_name=u"部门")
    reg_time = models.DateTimeField(auto_now_add=True)
    power = models.CharField(max_length=1, default='0', verbose_name=u"职阶")

    class Meta:
        db_table = "userinfo"
        verbose_name = u"用户注册信息"


# 日志表
class UserLog(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name=u"用户名")
    actionObject = models.CharField(max_length=20, verbose_name=u"操作对象")
    operationType = models.CharField(max_length=20, verbose_name=u"操作类型")
    ip = models.GenericIPAddressField(protocol='IPV4')
    logintime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log'
        verbose_name = u"登陆日志"


# 创建实例工单页
class instance_Orders(models.Model):
    id = models.AutoField(primary_key=True)
    created_user = models.CharField(max_length=30, default=None)
    instance_name = models.CharField(max_length=30)
    mem = models.IntegerField(default=1024)
    cpu = models.IntegerField(default=1)
    disk = models.IntegerField(default=50)
    bandwidth = models.CharField(max_length=10)
    os = models.CharField(max_length=30)
    storage = models.CharField(max_length=30, default='sas')
    expired = models.IntegerField(default=30)
    buy_number = models.IntegerField(default=1)
    dept = models.CharField(max_length=4, verbose_name=u"部门")
    apply_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'instance_orders'
        verbose_name = u"创建实例"


# 工单表
class worksheet(models.Model):
    id = models.AutoField(primary_key=True)
    add_time = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, default="申请云主机")
    username = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    dept = models.CharField(max_length=4, verbose_name=u"部门")
    Division_Manager = models.CharField(max_length=1, default=0)
    General_Manager = models.CharField(max_length=1, default=0)
    Cloud_Computing = models.CharField(max_length=1, default=0)
    class Mete:
        db_table = "worksheet"
        verbose_name = u"工单审核"


