# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vcloudapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='os',
            name='os_type',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]
