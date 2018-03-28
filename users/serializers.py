# -*- encoding: utf-8 -*-
"""
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
"""
