# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class qualificationsUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = qualifications_user
		fields = ('user','shop','order','rate',)
		read_only_fields = ('id','date_register',)

class qualificationsShopSerializer(serializers.ModelSerializer):
	class Meta:
		model = qualifications_shop
		fields = ('user','shop','order','rate',)
		read_only_fields = ('id','date_register',)
		