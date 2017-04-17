from __future__ import unicode_literals
from django.db import models
from django.conf import settings
from django.utils import timezone

# Create your models here.

class category(models.Model):
	name = models.CharField(max_length=60, blank=True)
	description = models.CharField(max_length=255, blank=True)
	picture = models.ImageField(upload_to="products",blank=True,null=True)
	class_icon = models.CharField(max_length=15,blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Categoria'
		verbose_name_plural = 'Categorias'

class subcategory(models.Model):
	category = models.ForeignKey(category)
	name = models.CharField(max_length=60, blank=True)
	description = models.CharField(max_length=255, blank=True)
	picture = models.ImageField(upload_to="products",blank=True,null=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Subcategoria'
		verbose_name_plural = 'Subcategorias'

class product(models.Model):
	subcategory = models.ForeignKey(subcategory)
	name = models.CharField(max_length=60, blank=True)
	suggested_price = models.CharField(max_length=10)
	description = models.CharField(max_length=255, blank=True)
	status = models.BooleanField(default=True)
	sku = models.CharField(max_length=255, blank=True)
	picture = models.ImageField(upload_to="products",blank=True,null=True)
	date_register = models.DateTimeField(auto_now_add=True)
	
	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
