# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-07 09:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcloudapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='power',
            name='dept_admin',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='power',
            name='dept_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='dept',
            field=models.CharField(default='other', max_length=255),
        ),
    ]