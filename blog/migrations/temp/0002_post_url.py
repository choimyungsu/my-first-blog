# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-19 00:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
