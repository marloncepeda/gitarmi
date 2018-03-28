# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-23 14:11
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.FloatField(default=0)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('date_register', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Profile user',
                'verbose_name_plural': 'Profiles users',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('date_register', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Status lists',
            },
        ),
        migrations.CreateModel(
            name='Types',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=255)),
                ('date_register', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'user types',
                'verbose_name_plural': 'List of user types',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Status'),
        ),
        migrations.AddField(
            model_name='profile',
            name='type_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Types'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]