from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from shopkeepers.models import info

class start(models.Model):
	name = models.CharField(max_length=40, blank=True)
	#shop = models.ForeignKey(info)
	code = models.CharField(max_length=20, blank=True)
	balance = models.CharField(max_length=15)
	quantity = models.CharField(max_length=15)
	description = models.CharField(max_length=255, blank=True)
	date_expire = models.DateTimeField(auto_now_add=False)
	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Cupon de inicio'
		verbose_name_plural = 'Cupones de inicio'

class personal(models.Model):
	name = models.CharField(max_length=40, blank=True)
	#shop = models.ForeignKey(info)
	code = models.CharField(max_length=20, blank=True)
	description = models.CharField(max_length=255, blank=True)
	balance = models.CharField(max_length=15)
	date_expire = models.DateTimeField(auto_now_add=False)
	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Cupon personal'
		verbose_name_plural = 'Cupones personales'

class promotional(models.Model):
	name = models.CharField(max_length=40, blank=True)
	#shop = models.ForeignKey(info)
	code = models.CharField(max_length=20, blank=True)
	balance = models.CharField(max_length=15)
	quantity = models.CharField(max_length=15)
	description = models.CharField(max_length=255, blank=True)
	date_expire = models.DateTimeField(auto_now_add=False)
	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Cupon promocional'
		verbose_name_plural = 'Cupones Promocionales'

class start_users_lists(models.Model):
	user = models.OneToOneField(User)
	coupon = models.ForeignKey(start)
	date_register = models.DateTimeField(auto_now_add=False)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Usuario cupon de inicio'
		verbose_name_plural = 'Listados de usuarios con cupones de inicio'

class personal_users_lists(models.Model):
	user = models.OneToOneField(User)
	coupon = models.ForeignKey(personal)
	date_register = models.DateTimeField(auto_now_add=False)
	
	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Usuario con cupon personal'
		verbose_name_plural = 'Listado de usuarios con cupones personales'

class promotional_users_lists(models.Model):
	user = models.OneToOneField(User)
	coupon = models.ForeignKey(promotional)
	date_register = models.DateTimeField(auto_now_add=False)

	#def __unicode__(self):
	#	return u"%s" % self.name

	class Meta:
		verbose_name = 'Usuario con cupon promocional'
		verbose_name_plural = 'Listado de usuarios con cupones promocionales'

class referralBonds(models.Model):
	pass

	class Meta:
		verbose_name = 'Balance de cuenta de usuario'
		verbose_name_plural = 'Balances de cuentas de usuarios'
