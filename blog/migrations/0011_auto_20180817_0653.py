# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-16 21:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20180817_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='attachment_ptr',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.AddField(
            model_name='post',
            name='id',
            field=models.AutoField(auto_created=True, default='', primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]