# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2018-03-02 14:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_task_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activities',
            options={'verbose_name': 'actividates', 'verbose_name_plural': 'listado de actividades'},
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
