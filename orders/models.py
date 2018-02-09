from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from users.models import Address, Types
from products.models import product
from shopkeepers.models import info, inventory

class status(models.Model):
	shop = models.ForeignKey(info)
	name = models.CharField(max_length=20, blank=True)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u"%s" % self.name

	class Meta:
		verbose_name = 'Estado de la orden'
		verbose_name_plural = 'Estados de las ordenes'


class Orders(models.Model):
	user = models.ForeignKey(User)
	user_address = models.ForeignKey(Address)
	shop = models.ForeignKey(info)
	total_quanty_products = models.IntegerField()
	time = models.DateTimeField('time delivery date', blank=True, null=True) #CharField(max_length=255)
	comment =models.CharField(max_length=50,blank=True)
	subtotal = models.CharField(max_length=12, blank=True)
	delivery_cost = models.CharField(max_length=12, blank=True)
	status_order = models.ForeignKey(status)
	method_pay = models.CharField(max_length=20, blank=True)
	total =models.DecimalField(max_digits=12, decimal_places=2,blank=False) #models.CharField(max_length=12, blank=True) 
	date_register = models.DateTimeField(auto_now_add=True)
	date_send = models.DateTimeField('send date', blank=True, null=True)
	date_confirm = models.DateTimeField('confirm date', blank=True, null=True)
	date_reject = models.DateTimeField('reject date', blank=True, null=True)
	date_end = models.DateTimeField('end date', blank=True, null=True)

	def __unicode__(self):
		return u"%s" % unicode(self.id)

	class Meta:
		verbose_name = 'Orden'
		verbose_name_plural = 'Ordenes'

class rejected_motive(models.Model):
	order = models.ForeignKey(Orders)
	motive = models.CharField(max_length=255)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return unicode(self.order)

	class Meta:
		verbose_name = 'Motivo de orden rechazada'
		verbose_name_plural = 'Motivos de las ordenes rechazadas'

class extended_order(models.Model):
	order = models.ForeignKey(Orders)
	product = models.ForeignKey(inventory)
	quanty =  models.IntegerField()
	price_unit = models.CharField(max_length=12, blank=True)
	subtotal = models.CharField(max_length=12, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return u"%s" % unicode(self.id)

	class Meta:
		verbose_name = 'Producto de la orden'
		verbose_name_plural = 'Productos de las ordenes'

class ticket_status(models.Model):
	name = models.CharField(max_length=20, blank=True)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
               return self.name

        class Meta:
                verbose_name = 'Estado del ticket'
                verbose_name_plural = 'Estado de los tickets'

class ticket_support(models.Model):
	type_user = models.ForeignKey(Types)
	order = models.ForeignKey(Orders)
	motive = models.CharField(max_length=2500, blank=False)
	status = models.ForeignKey(ticket_status)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
               return unicode(self.order)

        class Meta:
                verbose_name = 'Ticket de soporte de la orden'
                verbose_name_plural = 'Tickets de soporte de las ordenes'

