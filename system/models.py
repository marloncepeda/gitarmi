# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

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
	version = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return self.version

        class Meta:
                verbose_name = 'Terminos y condiciones'
                verbose_name_plural = 'Terminos y condiciones'
