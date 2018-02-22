# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User#, Profile
        fields = ('id', 'first_name', 'email',)
        password = serializers.CharField(write_only=True)
        write_only_fields = ('password',)
        read_only_fields = ('id',)
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
'''
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()
        return user
'''
class StatusSerializer(serializers.ModelSerializer):
	class Meta:
		model = Status
        fields = ('id','name','description','date_register',)
		

class StatusinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('id','name',)
        

class TypesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Types
		fields = ('id','name',)


class TypesinfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = ('name',)


class DevicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Devices
        fields = ('id','device', 'device_type','date_register',)


class WithoutShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Without_shops
        fields = ('id','email','lat','lon','device','device_type','date_register',)

class AddressSerializerFull(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','client','address_alias','address','address_detail','lat','lon','date_register',)

class AddressSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ('id','address','address_alias','address_detail','city')

class ProfileSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    type_user = TypesinfoSerializer()
    status = StatusinfoSerializer()
    class Meta:
        model = Profile
        fields = ('user','shop_name','phone','pictures','type_user','status','date_register','birthdate','rate')

class UsersSerializerBasic(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name','id')

class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = tags
        fields = ('name',) #'description','date_register',)
        #read_only_fields = ('id','date_register',)

class TagsBasicSerializer(serializers.ModelSerializer):
    tag = TagsSerializer()
    class Meta:
        model = users_tags
        fields = ('user','tag')
        #read_only_fields = ('id','date_register',)

class UserProfileSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    class Meta:
        model = Profile
        fields = ('user','pictures','rate')


