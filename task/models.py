from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
#from orders.models import Orders
#from shopkeepers.models import info


class statusTask(models.Model):
	name = models.CharField(max_length=150, blank=True)
	description = models.CharField(max_length=252, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return u"%s" % self.name
        class Meta:
                verbose_name = 'estado de la tarea'
                verbose_name_plural = 'listado de estados de la tarea'

class activities(models.Model):
	name = models.CharField(max_length=150, blank=True)
	fixed_price = models.CharField(max_length=150, blank=True)
	fixed_time = models.CharField(max_length=150, blank=True)
	extra_hour_price = models.CharField(max_length=150, blank=True)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return u"%s" % self.name
        class Meta:
                verbose_name = 'actividates'
                verbose_name_plural = 'listado de actividades'

class task(models.Model):
	client_id=models.ForeignKey(User)
    	date=models.CharField(max_length=150, blank=True)
    	startTime=models.CharField(max_length=150, blank=True)
    	address=models.CharField(max_length=150, blank=True)
   	address_details=models.CharField(max_length=150, blank=True)
    	lat=models.CharField(max_length=150, blank=True)
    	lng=models.CharField(max_length=150, blank=True)
    	city=models.CharField(max_length=150, blank=True)
    	activity_id=models.ForeignKey(activities)
    	job_description=models.CharField(max_length=150, blank=True)
    	notes_engineer=models.CharField(max_length=150, blank=True)
    	required_testing=models.CharField(max_length=150, blank=True)
    	site_contact=models.CharField(max_length=150, blank=True)
    	site_contact_number=models.CharField(max_length=150, blank=True)
	status = models.ForeignKey(statusTask)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
        	return '%s - %s' % (self.id, self.client_id) #return u"%s" % self.id
        class Meta:
        	verbose_name = 'tarea'
        	verbose_name_plural = 'listado de tareas'

class taskExtend(models.Model):
	engineer = models.ForeignKey(User)
	task = models.ForeignKey(task)
	date_register = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
                return u"%s" % self.task
        class Meta:
                verbose_name = 'asignar ingeniero'
                verbose_name_plural = 'Listado de ingenieros asignados'

class taskTrackingStatus(models.Model):
	task = models.ForeignKey(task)
	status =models.ForeignKey(statusTask)
	date_register = models.DateTimeField(auto_now_add=True)

        def __unicode__(self):
                return u"%s" % self.task
        class Meta:
                verbose_name = 'Historial status tarea'
                verbose_name_plural = 'Historial cambios de status de tareas'
#class qualifications_user(models.Model):
#	user = models.ForeignKey(User)
#	shop = models.ForeignKey(info)
#	order = models.ForeignKey(Orders)
#	rate = models.DecimalField(max_digits=12, decimal_places=1,blank=False)
#	comment = models.CharField(max_length=150, blank=True)
#	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

#	class Meta:
#		verbose_name = 'Calificar a el Usuario'
#		verbose_name_plural = 'Calificaciones de los usuarios'

#class qualifications_shop(models.Model):
#	user = models.ForeignKey(User)
#	shop = models.ForeignKey(info)
#	order = models.ForeignKey(Orders)
#	rate = models.DecimalField(max_digits=12, decimal_places=1,blank=False)
#	comment = models.CharField(max_length=150, blank=True)
#	date_register = models.DateTimeField(auto_now_add=True)

	#def __unicode__(self):
	#	return u"%s" % self.name

#	class Meta:
#		verbose_name = 'Calificar a la Tienda'
#		verbose_name_plural = 'Calificaciones de las Tiendas'
