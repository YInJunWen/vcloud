# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(max_length=20, verbose_name=u"用户名", primary_key=True)
    password = models.CharField(max_length=20, verbose_name=u"密码")
    email = models.EmailField(verbose_name=u"邮箱")
    dept = models.CharField(max_length=4, default='cp', verbose_name=u"部门")
    class Meta:
        db_table = "UserInfo"
        verbose_name = u"用户注册信息"


class Instance_Orders(models.Model):
    id = models.AutoField(primary_key=True)
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

class Logs(models.Model):
    id = models.AutoField(primary_key=True)
    log_type = models.CharField(max_length=20)
    opt_mode = models.CharField(max_length=20)
    opt_user = models.CharField(max_length=30)
    opt_ip = models.GenericIPAddressField(protocol='IPV4')

    class Meta:
        db_table = 'logs'


# class Test1(models.Model):
#     id = models.AutoField(primary_key=True)
#
#     class Meta:
#         db_table = 'test111'