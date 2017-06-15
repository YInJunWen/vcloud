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
    password = models.CharField(max_length=20, verbose_name=u"密码")
    email = models.EmailField(verbose_name=u"邮箱")
    dept = models.CharField(max_length=4, default='cp', verbose_name=u"部门")
    reg_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "userinfo"
        verbose_name = u"用户注册信息"


# 登陆日志表
class UserLog(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=20, verbose_name=u"用户名")
    logintime = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log'
        verbose_name = u"登陆日志"


# 创建实例工单页
class instance_Orders(models.Model):
    # username:  这个值没有读取到session
    id = models.AutoField(primary_key=True)
    # session 没值取不到 created_user = models.CharField(max_length=30, default=None)

    instance_name = models.CharField(max_length=30)
    mem = models.IntegerField(default=1024)
    cpu = models.IntegerField(default=1)
    disk = models.IntegerField(default=50)
    bandwidth = models.CharField(max_length=10)
    os = models.CharField(max_length=30)
    storage = models.CharField(max_length=30, default='sas')
    expired = models.IntegerField(default=30)

    class Meta:
        db_table = 'instance_orders'
        verbose_name = u"创建实例"
