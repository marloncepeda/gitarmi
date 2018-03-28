# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone


class Status(models.Model):
    name = models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=255, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status lists'

class Types(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)
    date_register = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'user types'
        verbose_name_plural = 'List of user types'

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    rate = models.FloatField(default=0)
    phone = models.CharField(max_length=20,blank=True)
    #pictures = models.ImageField(default='pictures_profile/default_avatar.png') #upload_to='pictures_profile'
    type_user = models.ForeignKey(Types)
    status = models.ForeignKey(Status)
    date_register = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Profile user'
        verbose_name_plural = 'Profiles users'

    def __unicode__(self):
        return self.phone
