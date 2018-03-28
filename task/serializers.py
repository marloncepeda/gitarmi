# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser
#from users.serializers import ProfileSerializer

from django.contrib.auth.models import User
#from shopkeepers.serializers import InfoShopMinSerializers
#from users.serializers import UsersSerializer
#from orders.serializers import OrderSerializerMinBasic

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


class activitiesSerializer(serializers.ModelSerializer):
        class Meta:
                model = activities
                fields = ('id','name','fixed_price','fixed_time','extra_hour_price',)

class statusSerializer(serializers.ModelSerializer):
	class Meta:
		model = statusTask
		fields =('id','name',)

class taskSerializer(serializers.ModelSerializer):
	client_id = UsersSerializer()
	activity_id = activitiesSerializer()
	class Meta:
		model = task
		fields = ('id','client_id','date','startTime','address','address_details','lat','lng','city','activity_id','job_description','notes_engineer','required_testing','site_contact','site_contact_number')

class taskStatusSerializer(serializers.ModelSerializer):
        status = statusSerializer()
	client_id = UsersSerializer()
        activity_id = activitiesSerializer()
        class Meta:
                model = task
                fields = ('id','client_id','date','startTime','address','address_details','lat','lng','city','activity_id','job_description','notes_engineer','required_testing','site_contact','site_contact_number','status')


class taskStatus2Serializer(serializers.ModelSerializer):
        client_id = UsersSerializer()
	status = statusSerializer()
        activity_id = activitiesSerializer()
        class Meta:
                model = task
                fields = ('id','client_id','date','startTime','address','address_details','lat','lng','city','activity_id','job_description','notes_engineer','required_testing','site_contact','site_contact_number','status')

class taskEngineerSerializer(serializers.ModelSerializer):
	#engineer = ProfileSerializer()
        task =taskStatus2Serializer()
	class Meta:
                model = taskExtend
                fields = ('engineer','task',)
#class activitiesSerializer(serializers.ModelSerializer):
#	class Meta:
#		model = activities
#		fields = ('id','name','fixed_price','fixed_time','extra_hour_price',)

#class qualificationsUserSerializer(serializers.ModelSerializer):
#	user = UsersSerializer()
#	shop = InfoShopMinSerializers()
#	order = OrderSerializerMinBasic()
#	class Meta:
#		model = qualifications_user
#		fields = ('user','shop','order','comment','rate',)
#		read_only_fields = ('id','date_register',)

#class qualificationsShopSerializer(serializers.ModelSerializer):
#	user = UsersSerializer()
 #       shop = InfoShopMinSerializers()
#        order = OrderSerializerMinBasic()

#	class Meta:
#		model = qualifications_shop
#		fields = ('user','shop','order','comment','rate',)
#		read_only_fields = ('id','date_register','comment','rate',)

