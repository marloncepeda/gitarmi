# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from users.serializers import UsersSerializerBasic, UserProfileSerializer, ProfileSerializer
from shopkeepers.serializers import InfoShopSerializers, InfoShopMinSerializers, InventorySerializers
from users.serializers import AddressSerializerBasic,TypesSerializer

class StatusSerializersFull(serializers.ModelSerializer):
	class Meta:
		model = status
		fields = ('name','description',)
		read_only_fields = ('id','date_register',)

class StatusSerializersBasic(serializers.ModelSerializer):
	class Meta:
		model = status
		fields = ('id','name',)

class OrderSerializerFull(serializers.ModelSerializer):
	user = UsersSerializerBasic()
	#shop = InfoShopSerializers()
	class Meta:
		model = Orders
		fields = ('id','user','user_address','method_pay','shop','total_quanty_products','delivery_cost','subtotal','total','date_register','comment',)
		read_only_fields = ('id','date_register')

class OrderSerializerFull2(serializers.ModelSerializer):
        user = UsersSerializerBasic()
        shop = InfoShopMinSerializers()
        class Meta:
                model = Orders
                fields = ('id','status_order','user','user_address','method_pay','shop','total_quanty_products','delivery_cost','subtotal','total','date_register','comment',)
                read_only_fields = ('id','date_register')

class OrderSerializerFull3(serializers.ModelSerializer):
        user = UsersSerializerBasic()
        shop = InfoShopSerializers()
	user_address = AddressSerializerBasic()
	status_order = StatusSerializersBasic()
        class Meta:
                model = Orders
                fields = ('id','status_order','user','user_address','method_pay','shop','total_quanty_products','delivery_cost','subtotal','total','date_register','date_send','date_confirm','date_reject','date_end','comment',)
                read_only_fields = ('id','date_register')

class OrderSerializerBasic2(serializers.ModelSerializer):
        #shop = InfoShopSerializers()
        #user_address = AddressSerializerBasic()
        status_order = StatusSerializersBasic()
        class Meta:
                model = Orders
                fields = ('time','status_order','shop','method_pay','total_quanty_products','subtotal','delivery_cost','total','date_register','comment',)
                read_only_fields = ('id','date_register')

class OrderSerializerBasic(serializers.ModelSerializer):
	user = UsersSerializerBasic()#UserProfileSerializer()
	user_address = AddressSerializerBasic()
	status_order = StatusSerializersBasic()
	class Meta:
		model = Orders
		fields = ('id','user','shop','user_address','method_pay','time','status_order','total_quanty_products','subtotal','delivery_cost','total','date_register','date_send','date_confirm','date_reject','date_end','comment',)
		read_only_fields = ('id','date_register')

class OrderSerializerWithShop(serializers.ModelSerializer):
        user = UsersSerializerBasic()#UserProfileSerializer()
        user_address = AddressSerializerBasic()
        status_order = StatusSerializersBasic()
	shop = InfoShopSerializers()
        class Meta:
                model = Orders
                fields = ('id','user','shop','user_address','method_pay','time','status_order','total_quanty_products','subtotal','delivery_cost','total','date_register','date_send','date_confirm','date_reject','date_end','comment',)
                read_only_fields = ('id','date_register')

class OrderSerializerBasic3(serializers.ModelSerializer):
        user = UsersSerializerBasic()#UserProfileSerializer()
        user_address = AddressSerializerBasic()
        status_order = StatusSerializersBasic()
        class Meta:
                model = Orders
                fields = ('id','user','user_address','method_pay','time','status_order','total_quanty_products','subtotal','delivery_cost','total','date_register','date_send','date_confirm','date_reject','date_end','comment',)

                read_only_fields = ('id','date_register')

class Extended_OrderSerializers(serializers.ModelSerializer):
	product = InventorySerializers()
	class Meta:
		model = extended_order
		fields = ('order','product','quanty','price_unit','subtotal',)
		read_only_fields = ('id','date_register',)

class ticketStatusSerializers(serializers.ModelSerializer):
        #product = InventorySerializers()
        class Meta:
                model =ticket_status
                fields = ('name','description',)
		read_only_fields = ('id','date_register',)

class ticketSupportSerializers(serializers.ModelSerializer):
        status = ticketStatusSerializers()
	order=OrderSerializerWithShop()
	type_user=TypesSerializer()
        class Meta:
                model = ticket_support
                fields = ('order','type_user','motive','status','date_register')
                read_only_fields = ('id','date_register',)
