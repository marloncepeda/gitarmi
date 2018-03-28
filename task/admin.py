from django.contrib import admin
from .models import *

#class qualificationsUserAdmin(admin.ModelAdmin):
	#search_fields = ('user_id__first_name','user_id__last_name', 'shop_id__name','id',)
#	list_display = ('id','user','shop','order','rate','comment','date_register')

class statusTaskAdmin(admin.ModelAdmin):
	list_display = ('id','name','description','date_register')

class ativitiesAdmin(admin.ModelAdmin):
	list_display = ('id','name','fixed_price','fixed_time','extra_hour_price')


class taskAdmin(admin.ModelAdmin):
        list_display = ('client_id','status')


class taskExtendAdmin(admin.ModelAdmin):
        list_display = ('task','engineer')

class taskTrackingStatusAdmin(admin.ModelAdmin):
        list_display = ('task','status')

admin.site.register(activities, ativitiesAdmin)
admin.site.register(task, taskAdmin)
admin.site.register(statusTask, statusTaskAdmin)
admin.site.register(taskExtend, taskExtendAdmin)
admin.site.register(taskTrackingStatus, taskTrackingStatusAdmin)
