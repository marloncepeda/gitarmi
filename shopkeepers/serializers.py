# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
from users.serializers import UsersSerializer
from products.serializers import ProductSerializersBasic, ProductSerializersWithImage, ProductSerializersWithImage2

class TypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = types
		fields = ('id','name','description','date_register',)

class statuSerializers(serializers.ModelSerializer):
    class Meta:
        model = statu
        fields = ('id','name',)#'description','date_register',)

class citySerializers(serializers.ModelSerializer):
    class Meta:
        model = city
        fields = ('id','name','picture',)

class cityAllSerializers(serializers.ModelSerializer):
    class Meta:
        model = city
        fields = ('id','name','description','picture',)

class InfoShopAllSerializers(serializers.ModelSerializer):
    user = UsersSerializer()
    city = citySerializers()
    class Meta:
        model = info
        fields = ('id','user','city','name','address','picture','type_shop','status_verify','rate','poly','objects','min_shipping_price',)

class InfoShopMinSerializers(serializers.ModelSerializer):
    class Meta:
        model = info
        fields = ('id','name','address','picture','min_price','phone','rate','cat_shop','average_deliveries', 'min_shipping_price',)

class StateSerializersBasic(serializers.ModelSerializer):
    class Meta:
        model = state
        fields = ('state',)

class StateSerializersFull(serializers.ModelSerializer):
    class Meta:
        model = state
        fields = ('id','shopkeeper','state','date_register',)

class TypeDeliveriesSerializers(serializers.ModelSerializer):
    class Meta:
        model = types_deliveries
        fields = ('id','name','description','time','date_register',)

class PriceDeliverySerializers(serializers.ModelSerializer):
    class Meta:
        model = price_delivery
        fields = ('id','shopkeeper','types','price','date_register',)

class InventorySerializers(serializers.ModelSerializer):
    product = ProductSerializersWithImage2() 
    class Meta:
        model = inventory
        fields = ('id','product','base_price','enable',)

class InventorySerializersFull(serializers.ModelSerializer):
    product = ProductSerializersWithImage2()
    class Meta:
        model = inventory
        fields = ('id','shop','product','base_price','enable',)

class InventorySerializersFullwithShop(serializers.ModelSerializer):
    product = ProductSerializersWithImage()
    shop = InfoShopMinSerializers()
    class Meta:
        model = inventory
        fields = ('id','shop','product','base_price','enable',)

class InventorySerializersBasic(serializers.ModelSerializer): 
    product = ProductSerializersBasic()
    class Meta:
        model = inventory
        fields = ('product','enable',)

class InfoShopSerializers(serializers.ModelSerializer):
    user = UsersSerializer()
    city = citySerializers()
    status_verify = statuSerializers()
    class Meta:
        model = info
        fields = ('id','user','city','name','address','phone','picture','min_price','stratum','status_verify','min_shipping_price','average_deliveries')

class InfoShopSerializersPoly(serializers.ModelSerializer):
    user = UsersSerializer()
    city = citySerializers()
    status_verify = statuSerializers()
    class Meta:
        model = info
        fields = ('id','user','city','name','address','phone','picture','min_price','stratum','status_verify','min_shipping_price','average_deliveries','poly','date_register')

class SchedulesSerializers(serializers.ModelSerializer):
    #user = UsersSerializer()
    #min_price =PriceDeliverySerializers()
    class Meta:
        model = schedules
        fields = ('day','work_hours','delivery_day',)

class CategoryShopSerializers(serializers.ModelSerializer):
    #shop = InfoShopMinSerializers()
    class Meta:
        model = category_shop
        fields = ('shop','category',)



class DocumentsSerializers(serializers.ModelSerializer):
    #shop = InfoShopMinSerializers()
    class Meta:
        model = documents
        fields = ('shop','cedula','rut','camara_comercio','recibo_servicio','type_client',)

class StatusExtendSerializers(serializers.ModelSerializer):
    #shop = InfoShopMinSerializers()
    class Meta:
        model = status_extend
        fields = ('shop','status','reason',)

