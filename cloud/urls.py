# -*- coding: utf-8 -*-
"""vcloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from vcloudapp.views import *

urlpatterns = {
    # url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='home'),  # 主页
    url(r'^login/$', userLogin, name='userLogin'),  # 登陆跳转
    url(r'^register/$', register, name='register'),  # 注册跳转
    url(r'^userLogin/$', userLogin, name='userLogin'),  # 用户登陆
    url(r'^userRegister/$', userRegister, name='userRegister'),  # 用户注册
    url(r'^checkLogin/$', checkLogin, name='checkLogin'),  # 验证登陆
    url(r'^get_password/$', get_password, name='get_password'),  # 找回密码
    url(r'^overview/$', overview, name='overview'),  # 概括页
    url(r'^instances/$', instances, name='instances'),  # 云主机页
    url(r'^disk/$', disk, name='disk'),  # 主盘
    url(r'^snapshot/$', snapshot, name='snapshot'),  # 快照
    url(r'^log/$', log, name='log'),  # 日志
    url(r'^order/$', order, name='order'),  # 工单
    url(r'^create_instance/$', create_instance, name='create_instance'),  # 创建实例跳转
    url(r'^chkcreate_instance/$', chkcreate_instance, name='chkcreate_instance'),  # 创建实例接口
    url(r'^zdgz/$', zdgz, name='zdgz'),
    # url(r'^/$', x, name='x'),
    # url(r'^/$', x, name='x'),
    # url(r'^/$', x, name='x'),
    # url(r'^/$', x, name='x'),
    # url(r'^/$', x, name='x'),
}