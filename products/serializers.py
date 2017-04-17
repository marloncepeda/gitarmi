# -*- encoding: utf-8 -*-
from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = category
		fields = ('id','name','description','picture','class_icon')
		read_only_fields = ('id','date_register')

class CategoryBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('id','name','picture')#eliminar picture luego
        #read_only_fields = ('id','date_register')
		
class SubcateorySerializer(serializers.ModelSerializer):
	category = CategorySerializer()
	class Meta:
		model = subcategory
		fields = ('id','category','name','description','picture',)
		read_only_fields = ('id','date_register')

class SubcateoryBasicSerializer(serializers.ModelSerializer):
    category = CategoryBasicSerializer()
    class Meta:
        model = subcategory
        fields = ('id','category','name',)
        #read_only_fields = ('id','date_register')

class ProductSerializersBasic(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('name','description')
        read_only_fields = ('id','date_register',)

class ProductSerializersFull(serializers.ModelSerializer):
    class Meta:
        model = product
        fields = ('id','name','description','sku','picture','date_register',)
        read_only_fields = ('id','date_register',)

class ProductSerializersWithImage(serializers.ModelSerializer):
    subcategory = SubcateoryBasicSerializer()
    class Meta:
        model = product
        fields = ('id','subcategory','name','description','picture','suggested_price',)

class ProductSerializersWithImage2(serializers.ModelSerializer):
    subcategory = SubcateoryBasicSerializer()
    class Meta:
        model = product
        fields = ('subcategory','name','description','picture','suggested_price',)


