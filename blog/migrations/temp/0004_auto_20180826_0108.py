# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-08-25 16:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_book_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='url',
            new_name='book_url',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='url',
            new_name='post_url',
        ),
    ]