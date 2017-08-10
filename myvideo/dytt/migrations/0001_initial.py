# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FailVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=20)),
                ('parentid', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'failvideo',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('picurl', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(max_length=20)),
                ('tag', models.CharField(max_length=20)),
                ('score', models.IntegerField(default=0)),
                ('qrytime', models.IntegerField(default=0)),
                ('parentid', models.IntegerField(default=0)),
                ('childsize', models.IntegerField(default=0)),
                ('isdone', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'video',
            },
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('name', 'tag')]),
        ),
        migrations.AlterUniqueTogether(
            name='failvideo',
            unique_together=set([('url', 'type')]),
        ),
    ]