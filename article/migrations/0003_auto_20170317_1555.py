# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 07:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20170316_2159'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='category',
            new_name='name',
        ),
    ]
