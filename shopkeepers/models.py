# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.db import models
from products.models import product

# Create your models here.
class types(models.Model):
	name = models.CharField(max_length=11,blank=False)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Tipo de vendedor'
		verbose_name_plural = 'Tipos de vendedor'

class statu(models.Model):
	name = models.CharField(max_length=10, blank=True)
	description = models.CharField(max_length=250, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Estado de verificación'
		verbose_name_plural = 'Estado de verificación'

class city(models.Model):
	name = models.CharField(max_length=10, blank=True)
	description = models.CharField(max_length=250, blank=True)
	picture = models.ImageField(upload_to="cities",blank=True,null=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name
	
	class Meta:
                verbose_name = 'Ciudad'
                verbose_name_plural = 'Ciudades'

class info(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	name = models.CharField(max_length=100)
	description = models.CharField(max_length=150)
	phone = models.CharField(max_length=20, default="",blank=True,null=True)
	city = models.ForeignKey(city,null=True)
	address = models.CharField(max_length=100,default="",blank=True,null=True)
	picture = models.ImageField(upload_to="shopkeepers",blank=True,null=True)
	type_shop = models.ForeignKey(types)
	status_verify = models.ForeignKey(statu)
	rate = models.FloatField(default=0)
	poly = models.PolygonField(blank=True,null=True)
	objects = models.GeoManager()
	min_price = models.CharField(max_length=10,blank=True)
	average_deliveries = models.CharField(max_length=10,blank=True)
	stratum = models.CharField(max_length=1,blank=True)
	min_shipping_price = models.CharField(max_length=30, blank=True)
	cat_shop = models.CharField(max_length=100,blank=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Vendedor'
		verbose_name_plural = 'Vendedores'

class category(models.Model):
	name = models.CharField(max_length=40)
	description = models.CharField(max_length=255, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Categoria'
		verbose_name_plural = 'Categorias'

class category_shop(models.Model):
	shop = models.ForeignKey(info)
	category = models.ForeignKey(category)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.shop.name

	class Meta:
		verbose_name = 'Categoria de vendedor'
		verbose_name_plural = 'Categorias de vendedores'

class state(models.Model):
	shopkeeper = models.ForeignKey(info)
	state = models.CharField(max_length=5,blank=False)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.shopkeeper.name

	class Meta:
		verbose_name = 'Estado'
		verbose_name_plural = 'Estado del vendedor [Abierto, Cerrado, Suspendido]'

class types_deliveries(models.Model):
	name = models.CharField(max_length=10,blank=False)
	description = models.CharField(max_length=255, blank=True)
	time = models.CharField(max_length=10,blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Tiempo de envio'
		verbose_name_plural = 'Tiempos de envios'

class price_delivery(models.Model):
	shopkeeper = models.ForeignKey(info)
	types = models.ForeignKey(types_deliveries)
	price = models.CharField(max_length=10,blank=False)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.shopkeeper.name

	class Meta:
		verbose_name = 'Precio de envio del vendedor'
		verbose_name_plural = 'Precios de envios del vendedor'

class types_client(models.Model):
	shop = models.ForeignKey(info)
	title = models.CharField(max_length=15)
	description = models.CharField(max_length=150)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.title

	class Meta:
		verbose_name = 'Tipo de catalogo'
		verbose_name_plural = 'Tipos de catalogos'

class lists_price(models.Model):
	shop = models.ForeignKey(info)
	type_client = models.ForeignKey(types_client)
	title =  models.CharField(max_length=15)
	price =models.CharField(max_length=5)	
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.shop

	class Meta:
		verbose_name = 'Lista de precio'
		verbose_name_plural = 'Listas de precios'

class inventory(models.Model):
	shop = models.ForeignKey(info)
	product = models.ForeignKey(product)
	enable = models.BooleanField()
	base_price = models.CharField(max_length=10)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(instance):
		return instance.product.name

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventario'

class lists_client(models.Model):
	shop = models.ForeignKey(info)
	type_client = models.ForeignKey(types_client)
	user = models.ForeignKey(User)
	description = models.CharField(max_length=150)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.shop

	class Meta:
		verbose_name = 'Listas de compradores'
		verbose_name_plural = 'Listas de compradores'

class schedules(models.Model):
	shop = models.ForeignKey(info)
	day = models.CharField(max_length=20, blank=False)
	work_hours = models.CharField(max_length=20, blank=True)
	delivery_day = models.BooleanField(default=False)
	date_register =  models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return self.shop

	class Meta:
		verbose_name = 'Horario de vendedor'
		verbose_name_plural = 'Horarios de vendedores'

class documents(models.Model):
	shop = models.ForeignKey(info)
	cedula = models.FileField(upload_to="users_docs/",blank=True,null=True)
	rut = models.FileField(upload_to="users_docs/",blank=True,null=True)
	camara_comercio = models.FileField(upload_to="users_docs/",blank=True,null=True)
	recibo_servicio = models.FileField(upload_to="users_docs/",blank=True,null=True)
	type_client = models.CharField(max_length=150)
	date_register =  models.DateTimeField(auto_now_add=True)
	
	class Meta:
                verbose_name = 'Documentos de la tienda'
                verbose_name_plural = 'Documentos de las tiendas'

class status_extend(models.Model):
	shop = models.ForeignKey(info)
	reason = models.CharField(max_length=255,blank=True,null=True)
	status = models.ForeignKey(statu)
	date_register =  models.DateTimeField(auto_now_add=True)

	class Meta:
                verbose_name = 'Historial estado de verificación'
                verbose_name_plural = 'Historiales de estados de verifiación'
