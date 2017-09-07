# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import hashlib

import datetime

import uuid as uuid
from django.db import models
from django.db import connection, transaction

# Create your models here.
# OpenStackDatabaseMeta


# 用户基本表
class UserInfo(models.Model):
    username = models.CharField(max_length=20, primary_key=True)  # 用户名
    password = models.CharField(max_length=50)  # 密码
    email = models.EmailField()  # 邮箱
    locked = models.BooleanField(max_length=1, default=False)  # True锁定账号, 不允许登陆
    power = models.IntegerField(default=0)  # 0-员工，1-主管，2-总经办，3-云计算中心
    role = models.IntegerField(default=1)  # 0-管理员，1-普通用户
    dept = models.CharField(max_length=50, default='other')  # 部门 默认云计算
    reg_ip = models.GenericIPAddressField(protocol='IPV4', max_length=15)  # 注册IP
    reg_time = models.DateTimeField(auto_now_add=True)  # 注册时间
    login_count = models.IntegerField(default=0)  # 登陆次数
    instances_count = models.IntegerField(default=0)  # 实例数量
    last_ip = models.CharField(max_length=15, default='0.0.0.0')  # 最后登录ip
    last_time = models.DateTimeField(auto_now_add=True)  # 最后登录时间 Now()
    id_card = models.CharField(max_length=18, default='000000000000000000')
    u_phone = models.CharField(max_length=11, default='00000000000')

    class Meta:
        db_table = "user_info"


# 部门信息表
class Dept(models.Model):
    dept_name = models.CharField(max_length=20)  # 部门简称
    dept_friendname = models.CharField(max_length=20)  # 部门员工
    dept_leader = models.CharField(max_length=20)  # 部门主管 多个用逗号分隔

    class Meta:
        db_table = "dept"


# 订单
class Order(models.Model):
    pid = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)  # 创建日期
    created_user = models.CharField(max_length=20)  # 创建人
    expired_at = models.DateTimeField()  # 此订单有效日期, 超过则失效
    dept_pending = models.IntegerField(default=1)  # 部门审核 0-已审核 1-未审核
    admin_pending = models.IntegerField(default=1)  # 总经办
    vcloud_pending = models.IntegerField(default=1)  # 云计算审核
    status = models.IntegerField(default=1)  # 0-已完成，1-审核中，2-已过期
    uuid = models.UUIDField()  # 订单明细 uuid关联订单明细用
    payed = models.IntegerField(default=1)  # 支付确认 0-已支付 1-未支付
    dept = models.CharField(max_length=20)
    # visibility = models.BooleanField(default=0)  # 0-不可见

    class Meta:
        db_table = "order"


# 订单明细
class OrderDetail(models.Model):
    pid = models.AutoField(primary_key=True)
    uuid = models.UUIDField()
    vcpu = models.IntegerField(default=1)  # cpu
    memory = models.IntegerField(default=1)  # 内存
    bandwidth = models.IntegerField()
    os = models.IntegerField()  # os.pid
    disk = models.IntegerField(default=0)  # disk.pid
    password = models.CharField(max_length=20)
    expire = models.IntegerField(default=30)  # 购买时长
    network = models.CharField(max_length=20)
    price = models.FloatField(default=0)
    flavor = models.CharField(max_length=20)

    class Meta:
        db_table = "order_detail"


# 操作系统
class OS(models.Model):
    pid = models.AutoField(primary_key=True)
    os_name = models.CharField(max_length=255)  # 后端显示系统名称
    os_friendname = models.CharField(max_length=255)  # 后端显示系统名
    os_type = models.CharField(max_length=20)

    class Meta:
        db_table = "os"


# 日志
class Log(models.Model):
    pid = models.AutoField(primary_key=True)
    log_type = models.IntegerField()  # 日志类型 log_type.log_id
    log_opt = models.DateTimeField(auto_now_add=True)  # 操作时间
    log_user = models.CharField(max_length=20)  # 操作者
    log_detail = models.CharField(max_length=255, default="")  # 日志内容
    log_shown = models.BooleanField(default=True)  # true 显示   false 隐藏
    log_ip = models.CharField(max_length=15, default='0.0.0.0')  # 登陆ip

    class Meta:
        db_table = "log"


# 日志类型
class LogType(models.Model):
    log_name = models.CharField(max_length=20)  # 日志类型
    log_id = models.IntegerField()  # 0-登录，1-实例，2-磁盘，3-快照，4-系统

    class Meta:
        db_table = "log_type"


# 实例订单
class Instances(models.Model):
    pid = models.AutoField(primary_key=True)
    create_at = models.DateTimeField()  # 申请时间
    expired_at = models.DateTimeField()  # 申请时常
    delayed_at = models.DateTimeField()  # 到期未续后宽限时间
    belonged = models.CharField(max_length=20)  # 创建者 属于
    name = models.CharField(max_length=20)  # 实例名称
    uuid = models.UUIDField(default=uuid.uuid4, max_length=36)  # 实例uuid
    vcpus = models.IntegerField(default=1)
    memory = models.IntegerField(default=1)
    bandwidth = models.IntegerField()
    os = models.IntegerField()
    disk = models.IntegerField(default=1)
    status = models.IntegerField(default=0)  # 0=running,1=stopped
    locked = models.BooleanField(default=False)  # true=到期未续后锁定，用户无法解锁

    class Meta:
        db_table = "instances"


# IP地址
class IP(models.Model):
    pid = models.AutoField(primary_key=True)
    uuid = models.UUIDField(default=uuid.uuid4, max_length=36)  # 唯一识别码
    mac_address = models.CharField(max_length=15, default='0000-0000-0000')  # 网卡地址
    ip_address = models.GenericIPAddressField(max_length=15, default='0.0.0.0')
    traffice_in = models.IntegerField(default=0)  # 流量进
    traffice_out = models.IntegerField(default=0)  # 流量出

    class Meta:
        db_table = "ip"


# 快照
class Snapshot(models.Model):
    pid = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    belonged = models.CharField(max_length=255)  # 实例
    status = models.IntegerField(default=0)  # 0-正常 1-无效 2-删除

    class Meta:
        db_table = "snapshot"


# 快照计数
class SnapshotCount(models.Model):
    pid = models.AutoField(primary_key=True)
    instance_name = models.CharField(max_length=20)
    snapshot_count = models.IntegerField(default=0)  # 实例快照数 最大3个 超过三个不能创建

    class Meta:
        db_table = "snapshot_count"


# 网络
class Network(models.Model):
    pid = models.AutoField(primary_key=True)
    dis_playname = models.CharField(max_length=50)
    net_name = models.CharField(max_length=20)
    net_desc = models.CharField(max_length=20)
    # uuid = models.UUIDField(uuid.uuid4, max_length=36)

    class Meta:
        db_table = "network"


# 实力类型
class InsFlavor(models.Model):
    pid = models.AutoField(primary_key=True)
    display_name = models.CharField(max_length=20)
    flavor_name = models.CharField(max_length=20)
    uuid = models.UUIDField(uuid.uuid4, max_length=36)

    class Meta:
        db_table = 'ins_flavor'


# 部门领导
class Power(models.Model):
    dept_name = models.CharField(max_length=255)
    dept_admin = models.CharField(max_length=255)

    class Meta:
        db_table = 'power'


# 邮箱验证
class CheckCode(models.Model):
    email = models.EmailField(primary_key=True)
    code = models.CharField(max_length=8)

    class Meta:
        db_table = 'check_code'


# return

