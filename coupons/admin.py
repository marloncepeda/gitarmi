from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from products.models import product
from shopkeepers.models import info

# Register your models here.
class startAdmin(admin.ModelAdmin):
	search_fields = ('id','name','code', 'description','date_expire',)
	list_display = ('id','name','code','balance','quantity', 'description','date_expire','date_register')

class personalAdmin(admin.ModelAdmin):
	search_fields = ('id','name','code', 'description','date_expire',)
	list_display = ('id','name','code','balance','description','date_expire','date_register')

class promotionalAdmin(admin.ModelAdmin):
	search_fields = ('id','name','code', 'description','date_expire',)
	list_display = ('id','name','code','balance','quantity','description','date_expire','date_register')

class start_users_listsAdmin(admin.ModelAdmin):
	search_fields = ('id','name_buyer','coupon',)
	list_display = ('id','name_buyer','coupon', 'date_register')

	def name_buyer(self, instance):
		return instance.user.first_name

class personal_users_listsAdmin(admin.ModelAdmin):
	search_fields = ('id','name_buyer','coupon',)
	list_display = ('id','name_buyer','coupon', 'date_register')

	def name_buyer(self, instance):
		return instance.user.first_name
		
class promotional_users_listsAdmin(admin.ModelAdmin):
	search_fields = ('id','name_buyer','coupon',)
	list_display = ('id','name_buyer','coupon', 'date_register')

	def name_buyer(self, instance):
		return instance.user.first_name
		
class referralBondsAdmin(admin.ModelAdmin):
	pass

admin.site.register(start, startAdmin)
admin.site.register(personal, personalAdmin)
admin.site.register(promotional, promotionalAdmin)
admin.site.register(start_users_lists, start_users_listsAdmin)
admin.site.register(personal_users_lists, personal_users_listsAdmin)
admin.site.register(promotional_users_lists, promotional_users_listsAdmin)
admin.site.register(referralBonds, referralBondsAdmin)