from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from products.models import product
from shopkeepers.models import info

# Register your models here.

class orderAdmin(admin.ModelAdmin):
	search_fields = ('user_id__first_name','user_id__last_name', 'shop_id__name','id',)
	list_display = ('id','name_buyer','shop','time','status_order','method_pay','total_quanty_products','subtotal','delivery_cost','total','date_register')

	def name_buyer(self, instance):
		return instance.user.first_name

class extended_orderAdmin(admin.ModelAdmin):
	search_fields = ('order', 'quanty','product_id__name',)
	list_display = ('order', 'product','price_unit','quanty','subtotal','date_register')

class statusAdmin(admin.ModelAdmin):
	search_fields = ('name', 'description',)
	list_display = ('name', 'description','date_register')

	#def product_name(self, instance):
	#	return instance.product.name

class rejectedMotiveAdmin(admin.ModelAdmin):
	search_fields = ('order', 'motive',)
	list_display = ('order', 'motive','date_register')

class ticketStatusAdmin(admin.ModelAdmin):
        search_fields = ('name', 'description',)
        list_display = ('name', 'description','date_register')

class ticketSupportAdmin(admin.ModelAdmin):
        search_fields = ('order', 'motive','status',)
        list_display = ('order','buyer__name','type_user','motive','status','date_register')
	
	def buyer__name(self, instance):
		return instance.order.user


admin.site.register(Orders, orderAdmin)
admin.site.register(extended_order, extended_orderAdmin)
admin.site.register(status, statusAdmin)
admin.site.register(rejected_motive, rejectedMotiveAdmin)
admin.site.register(ticket_status, ticketStatusAdmin)
admin.site.register(ticket_support, ticketSupportAdmin)

