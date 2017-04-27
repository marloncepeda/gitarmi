# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class Status(models.Model):
    name = models.CharField(max_length=30,blank=False)
    description = models.CharField(max_length=255, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Status'

class Types(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=255, blank=True)
    date_register = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Tipo de Usuario'
        verbose_name_plural = 'Tipos de Usuarios'
        
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    phone = models.CharField(max_length=12,blank=True)
    pictures = models.ImageField(upload_to='pictures_profile',default='images/static/profile.png')
    birthdate = models.CharField(max_length=10,blank=False)
    type_user = models.ForeignKey(Types)
    status = models.ForeignKey(Status)
    date_register = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Perfil Usuario'
        verbose_name_plural = 'Perfiles de Usuarios'

    def __unicode__(self):
        return self.phone

class Devices(models.Model):
	user = models.OneToOneField(settings.AUTH_USER_MODEL)
	device = models.TextField(blank=True,null=True)
	device_type = models.CharField(max_length=10,blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

class Without_shops(models.Model):
	email = models.EmailField(blank=True,null=True)
	lat = models.CharField(max_length=100,default="",blank=True,null=True)
	lon = models.CharField(max_length=100,default="",blank=True,null=True)
	device = models.TextField(blank=True,null=True)
	device_type = models.TextField(blank=True,null=True,default="android")
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.email

	class Meta:
		verbose_name = 'Usuarios sin tienda'
		verbose_name_plural = 'Usuarios sin tiendas cercanas'

class Address(models.Model):
    client = models.ForeignKey(User)
    address_alias = models.CharField(max_length=11,blank=True)
    address = models.CharField(max_length=100, blank=True)
    address_detail = models.CharField(max_length=100,blank=True,null=True)
    lat = models.CharField(max_length=100,default="",blank=True,null=True)
    lon = models.CharField(max_length=100,default="",blank=True,null=True)
    date_register = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.address

    class Meta:
        verbose_name = 'Dirección'
        verbose_name_plural = 'Direcciones'

class tags(models.Model):
    name = models.CharField(max_length=50, blank=False)
    description = models.CharField(max_length=50, blank=True)
    date_register = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = 'Crear etiqueta'
        verbose_name_plural = 'Creación de etiquetas'


class users_tags(models.Model):
    user = models.ForeignKey(User)
    tag = models.ForeignKey(tags)
    date_register = models.DateTimeField(auto_now_add=True)

    #def __unicode__(self):
    #    return self.user

    class Meta:
        verbose_name = 'Etiquetas de usuario'
        verbose_name_plural = 'Etiquetas de usuarios'
