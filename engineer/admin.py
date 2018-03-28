
from django.contrib import admin
from .models import *
from django.contrib.auth.models import User

class engiProfileAdmin(admin.ModelAdmin):
	search_fields = ('id','user','company',)
	list_display = ('id','user','company', 'date_register')

	#def name_buyer(self, instance):
	#	return instance.user.first_name

class statusAdmin(admin.ModelAdmin):
	search_fields = ('id','name',)
	list_display = ('id','name', 'date_register')

	#def name_buyer(self, instance):
	#	return instance.user.first_name

class statusEngineerAdmin(admin.ModelAdmin):
	search_fields = ('id','engineer','date_register',)
	list_display = ('id','engineer','status', 'date_register')

admin.site.register(engiProfile, engiProfileAdmin)
admin.site.register(status, statusAdmin)
admin.site.register(statusEngineer, statusEngineerAdmin)

