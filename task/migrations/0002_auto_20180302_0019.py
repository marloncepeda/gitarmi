# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-03-02 00:19
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activities',
            old_name='nano',
            new_name='name',
        ),
    ]
