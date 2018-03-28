from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class engiProfile(models.Model):
	user = models.ForeignKey(User)
	phone = models.CharField(max_length=40, blank=True)
	company = models.CharField(max_length=140, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	#picture

	def __unicode__(self):
		return u"%s" % self.phone

	class Meta:
		verbose_name = 'Perfil ingeniero'
		verbose_name_plural = 'Listado de perfiles'

class status(models.Model):
	name = models.CharField(max_length=40, blank=True)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		verbose_name = 'Estado del ingeniero'
		verbose_name_plural = 'Listado Estados del ingeniero'

class statusEngineer(models.Model):
        engineer = models.ForeignKey(engiProfile)
        status = models.ForeignKey(status)
        date_register = models.DateTimeField(auto_now_add=True)

        def __unicode__(self):
               return u"%s" % self.status

	class Meta:
                verbose_name = 'Estado del ingeniero'
                verbose_name_plural = 'Listado Estados del ingeniero'
