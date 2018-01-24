# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from shopkeepers.models import info

class company(models.Model):
        name = models.CharField(max_length=11,blank=False)
	picture = models.ImageField(upload_to="company",blank=True,null=True)
	address = models.CharField(max_length=255, blank=True)
        description = models.CharField(max_length=255, blank=True)
	phone1 = models.CharField(max_length=255, blank=False)
	phone2 = models.CharField(max_length=255, blank=True)
	phone3 = models.CharField(max_length=255, blank=True)
	phone4 = models.CharField(max_length=255, blank=True)
	email =  models.CharField(max_length=255, blank=True)
        date_register = models.DateTimeField(auto_now_add=True)

        def __unicode__(self):
                return self.name

        class Meta:
                verbose_name = 'Datos de las empresas'
                verbose_name_plural = 'Datos de la empresa'

class termsAndConditions(models.Model):
	document = models.FileField(upload_to="terms",blank=True,null=True)
	file = models.FileField(upload_to="system/",blank=True,null=True)
	version = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return self.version

        class Meta:
                verbose_name = 'Terminos y condiciones'
                verbose_name_plural = 'Terminos y condiciones'

class statusRequestingCalls(models.Model):
	name= models.CharField(max_length=30, blank=True)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
                return self.name

        class Meta:
                verbose_name = 'Estados de las llamadas'
                verbose_name_plural = 'Estado de la llamada'

class requestingCallsToUsers(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	status = models.ForeignKey(statusRequestingCalls)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
                return self.user

        class Meta:
                verbose_name = 'Solicitudes de llamadas de usuarios'
                verbose_name_plural = 'Solicitud de llamada de usuario'

class requestingCallsToShops(models.Model):
        shop = models.ForeignKey(info)
        status = models.ForeignKey(statusRequestingCalls)
        date_register = models.DateTimeField(auto_now_add=True)

        def __unicode__(self):
                return self.user

        class Meta:
                verbose_name = 'Solicitudes de llamadas de tenderos'
                verbose_name_plural = 'Solicitud de llamada de tendero'



class appVersions(models.Model):
	version = models.CharField(max_length=255, blank=True)
	type = models.CharField(max_length=255, blank=True)
	status = models.BooleanField()
	date_register = models.DateTimeField(auto_now_add=True)

	class Meta:
                verbose_name = 'Versiones de las aplicaciones'
                verbose_name_plural = 'Version de la app'

