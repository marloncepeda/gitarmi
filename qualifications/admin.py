from django.contrib import admin
from .models import *

class qualificationsUserAdmin(admin.ModelAdmin):
	#search_fields = ('user_id__first_name','user_id__last_name', 'shop_id__name','id',)
	list_display = ('id','user','shop','order','rate','comment','date_register')

class qualificationsShopAdmin(admin.ModelAdmin):
	list_display = ('id','user','shop','order','rate','comment','date_register')

admin.site.register(qualifications_user, qualificationsUserAdmin)
admin.site.register(qualifications_shop, qualificationsShopAdmin)