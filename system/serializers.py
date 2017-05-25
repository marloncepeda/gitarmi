# -*- encoding: utf-8 -*-

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework import permissions
from rest_framework.permissions import IsAdminUser

class CompanySerializer(serializers.ModelSerializer):
        class Meta:
                model = company
                fields = ('id','name','description','picture','address','phone1','phone2','phone3','phone4','email','date_register',)

class CompanyPhonesSerializer(serializers.ModelSerializer):
        class Meta:
                model = company
                fields = ('name','phone1','phone2','phone3','phone4',)

class TermsSerializer(serializers.ModelSerializer):
        class Meta:
                model = termsAndConditions
                fields = ('id','version','file','document','date_register',)

class statusRequestingCallsSerializer(serializers.ModelSerializer):
        class Meta:
                model = statusRequestingCalls
                fields = ('id','name','description','date_register',)

class requestingCallsToUsersSerializer(serializers.ModelSerializer):
        class Meta:
                model = requestingCallsToUsers
                fields = ('id','user','status','date_register',)

class requestingCallsToShopsSerializer(serializers.ModelSerializer):
        class Meta:
                model = requestingCallsToShops
                fields = ('id','shop','status','date_register')
