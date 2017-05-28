# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from shopkeepers.serializers import InfoShopMinSerializers
from users.serializers import UsersSerializer
from orders.serializers import OrderSerializerMinBasic

class qualificationsUserSerializer(serializers.ModelSerializer):
	user = UsersSerializer()
	shop = InfoShopMinSerializers()
	order = OrderSerializerMinBasic()
	class Meta:
		model = qualifications_user
		fields = ('user','shop','order','comment','rate',)
		read_only_fields = ('id','date_register',)

class qualificationsShopSerializer(serializers.ModelSerializer):
	user = UsersSerializer()
        shop = InfoShopMinSerializers()
        order = OrderSerializerMinBasic()

	class Meta:
		model = qualifications_shop
		fields = ('user','shop','order','comment','rate',)
		read_only_fields = ('id','date_register','comment','rate',)
		
