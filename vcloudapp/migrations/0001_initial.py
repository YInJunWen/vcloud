# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dept_name', models.CharField(max_length=20)),
                ('dept_friendname', models.CharField(max_length=20)),
                ('dept_leader', models.CharField(max_length=20)),
            ],
            options={
                'db_table': 'dept',
            },
        ),
        migrations.CreateModel(
            name='InsFlavor',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=20)),
                ('flavor_name', models.CharField(max_length=20)),
                ('uuid', models.UUIDField(verbose_name=uuid.uuid4)),
            ],
            options={
                'db_table': 'ins_flavor',
            },
        ),
        migrations.CreateModel(
            name='Instances',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('create_at', models.DateTimeField()),
                ('expired_at', models.DateTimeField()),
                ('delayed_at', models.DateTimeField()),
                ('belonged', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('vcpus', models.IntegerField(default=1)),
                ('memory', models.IntegerField(default=1)),
                ('bandwidth', models.IntegerField()),
                ('os', models.IntegerField()),
                ('disk', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=0)),
                ('locked', models.BooleanField(default=False)),
            ],
            options={
                'db_table': 'instances',
            },
        ),
        migrations.CreateModel(
            name='IP',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('mac_address', models.CharField(default='0000-0000-0000', max_length=15)),
                ('ip_address', models.GenericIPAddressField(default='0.0.0.0')),
                ('traffice_in', models.IntegerField(default=0)),
                ('traffice_out', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'ip',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('log_type', models.IntegerField()),
                ('log_opt', models.DateTimeField(auto_now_add=True)),
                ('log_user', models.CharField(max_length=20)),
                ('log_detail', models.CharField(default='', max_length=255)),
                ('log_shown', models.BooleanField(default=True)),
                ('log_ip', models.CharField(default='0.0.0.0', max_length=15)),
            ],
            options={
                'db_table': 'log',
            },
        ),
        migrations.CreateModel(
            name='LogType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_name', models.CharField(max_length=20)),
                ('log_id', models.IntegerField()),
            ],
            options={
                'db_table': 'log_type',
            },
        ),
        migrations.CreateModel(
            name='Network',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('dis_playname', models.CharField(max_length=50)),
                ('net_name', models.CharField(max_length=20)),
                ('net_desc', models.CharField(max_length=20)),
                ('uuid', models.UUIDField(verbose_name=uuid.uuid4)),
            ],
            options={
                'db_table': 'network',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_user', models.CharField(max_length=20)),
                ('expired_at', models.DateTimeField(auto_now_add=True)),
                ('dept_pending', models.IntegerField(default=1)),
                ('admin_pending', models.IntegerField(default=1)),
                ('vcloud_pending', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=1)),
                ('uuid', models.UUIDField()),
                ('payed', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('uuid', models.UUIDField()),
                ('vcpu', models.IntegerField(default=1)),
                ('memory', models.IntegerField(default=1)),
                ('bandwidth', models.IntegerField()),
                ('os', models.IntegerField()),
                ('disk', models.IntegerField(default=0)),
                ('password', models.CharField(max_length=20)),
                ('expire', models.IntegerField(default=30)),
                ('network', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'order_detail',
            },
        ),
        migrations.CreateModel(
            name='OS',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('os_name', models.CharField(max_length=255)),
                ('os_friendname', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'os',
            },
        ),
        migrations.CreateModel(
            name='Snapshot',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('display_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('belonged', models.CharField(max_length=255)),
                ('status', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'snapshot',
            },
        ),
        migrations.CreateModel(
            name='SnapshotCount',
            fields=[
                ('pid', models.AutoField(primary_key=True, serialize=False)),
                ('instance_name', models.CharField(max_length=20)),
                ('snapshot_count', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'snapshot_count',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('locked', models.BooleanField(default=False, max_length=1)),
                ('power', models.IntegerField(default=0)),
                ('role', models.IntegerField(default=1)),
                ('dept', models.CharField(default='other', max_length=4)),
                ('reg_ip', models.GenericIPAddressField(protocol='IPV4')),
                ('reg_time', models.DateTimeField(auto_now_add=True)),
                ('login_count', models.IntegerField(default=0)),
                ('instances_count', models.IntegerField(default=0)),
                ('last_ip', models.CharField(default='0.0.0.0', max_length=15)),
                ('last_time', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'user_info',
            },
        ),
    ]
