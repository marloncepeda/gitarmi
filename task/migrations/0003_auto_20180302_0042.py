# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-03-02 00:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_auto_20180302_0019'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='description',
            new_name='extra_hour_price',
        ),
        migrations.AddField(
            model_name='activities',
            name='fixed_price',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='activities',
            name='fixed_time',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
