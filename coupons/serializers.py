# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class startSerializers(serializers.ModelSerializer):
	class Meta:
		model = start
		fields = ('name','code', 'description','date_expire')
		read_only_fields = ('id','date_register',)

class personalSerializers(serializers.ModelSerializer):
	class Meta:
		model = personal
		fields = ('name','code', 'description','date_expire')
		read_only_fields = ('id','date_register',)

class promotionalSerializers(serializers.ModelSerializer):
	class Meta:
		model = promotional
		fields = ('name','code', 'description','date_expire')
		read_only_fields = ('id','date_register',)

class startUsersListsSerializers(serializers.ModelSerializer):
	class Meta:
		model = start_users_lists
		fields = ('user','coupon',)
		read_only_fields = ('id','date_register',)

class personalUsersListsSerializers(serializers.ModelSerializer):
	class Meta:
		model = personal_users_lists
		fields = fields = ('user','coupon',)
		read_only_fields = ('id','date_register',)
		
class promotionalUsersListsSerializers(serializers.ModelSerializer):	
	class Meta:
		model = promotional_users_lists
		fields = fields = ('user','coupon',)
		read_only_fields = ('id','date_register',)	

class referralBondsSerializers(serializers.ModelSerializer):
	pass

