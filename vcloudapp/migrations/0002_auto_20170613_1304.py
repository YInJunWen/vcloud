# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-13 05:04
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vcloudapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userinfo',
            options={'verbose_name': '\u7528\u6237\u6ce8\u518c\u4fe1\u606f'},
        ),
        migrations.AlterModelTable(
            name='userinfo',
            table='UserInfo',
        ),
    ]
