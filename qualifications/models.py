from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from orders.models import Orders
from shopkeepers.models import info

class qualifications_user(models.Model):
	user = models.ForeignKey(User)
	shop = models.ForeignKey(info)
	order = models.ForeignKey(Orders)
	rate = models.CharField(max_length=10)
	comment = models.CharField(max_length=150, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Calificar a el Usuario'
		verbose_name_plural = 'Calificaciones de los usuarios'

class qualifications_shop(models.Model):
	user = models.ForeignKey(User)
	shop = models.ForeignKey(info)
	order = models.ForeignKey(Orders)
	rate = models.CharField(max_length=10)
	comment = models.CharField(max_length=150, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Calificar a la Tienda'
		verbose_name_plural = 'Calificaciones de las Tiendas'
