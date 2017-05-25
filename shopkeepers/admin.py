from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.gis import admin
from django.contrib.gis.geos import GEOSGeometry
# Register your models here.

class TypesAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description','date_register', )

class StateAdmin(admin.ModelAdmin):
    search_fields = ('shopkeeper', 'state',)
    list_display = ('shopkeeper', 'state','date_register', )

class StatuAdmin(admin.ModelAdmin):
    search_fields = ('name', 'date_register',)
    list_display = ('name','description','date_register', )

class CityAdmin(admin.ModelAdmin):
    search_fields = ('name', 'date_register',)
    list_display = ('name','description','date_register', )

class InfoAdmin(admin.ModelAdmin):
    search_fields = ('name','rate','user_id__first_name')
    list_display = ('name','first_name','city','last_name','user_email', 'address','type_shop','rate','date_register','min_price','average_deliveries','stratum','min_shipping_price','picture','poly',)

    def user_email(self, instance):
    	return instance.user.email

    def first_name(self, instance):
    	return instance.user.first_name

    def last_name(self, instance):
    	return instance.user.last_name

    extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"] 
    map_template = 'gmgdav3.html'

class TypesDeliveriesAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description','time','data_register',)
    list_display = ('name','description','time', 'date_register',)

class PriceDeliveryAdmin(admin.ModelAdmin):
    search_fields = ('shopkeeper', 'types','price','data_register',)
    list_display = ('shopkeeper_name','types','price', 'date_register',)

    def shopkeeper_name(self, instance):
        return instance.shopkeeper.name

class TypesClientAdmin(admin.ModelAdmin):
    search_fields = ('shop','title','description',) 
    list_display = ('shop','title','description',)

    def shopkeeper_name(self, instance):
        return instance.shopkeeper.name

class ListsPriceAdmin(admin.ModelAdmin):
    search_fields = ('shop','type_client','title','price','date_register',)
    list_display = ('shopkeeper_name','type_client','title','price','date_register',)
    
    def shopkeeper_name(self, instance):
        return instance.shopkeeper.name

class InventoryAdmin(admin.ModelAdmin):
    search_fields = ('shop','product','base_price','date_register',)
    list_display = ('shopkeeper_name','product_name','base_price','date_register',)

    def shopkeeper_name(self, instance):
        return instance.shop.name

    def product_name(self, instance):
        return instance.product.name
        
class ListsClientAdmin(admin.ModelAdmin):
    search_fields =('shop','type_client','user','description','date_register',)
    list_display =('shop','type_client','user','description','date_register',)

class SchedulesAdmin(admin.ModelAdmin):
    search_fields =('shop','day','work_hours','delivery_day','date_register',)
    list_display =('shop','day','work_hours','delivery_day','date_register',)


class CategoryAdmin(admin.ModelAdmin):
    search_fields =('name','description','date_register',)
    list_display =('name','description','date_register',)

class CategoryShopAdmin(admin.ModelAdmin):
    search_fields =('shop','category','date_register',)
    list_display =('shop','category','date_register',)

class DocumentShopAdmin(admin.ModelAdmin):
    search_fields =('shop','date_register',)
    list_display =('shop','cedula','rut','camara_comercio','recibo_servicio','type_client','date_register',)

class statusExtendAdmin(admin.ModelAdmin):
    search_fields =('shop','status','date_register',)
    list_display =('shop','status','date_register',)

class methodPaymentAdmin(admin.ModelAdmin):
    search_fields =('name','status','date_register',)
    list_display =('name','description','status','date_register',)

class shopMethodPaymentAdmin(admin.ModelAdmin):
    search_fields =('shop','status','date_register',)
    list_display =('shop','method_pay','status','date_register',)

admin.site.register(types,TypesAdmin)
admin.site.register(state, StateAdmin)
admin.site.register(statu, StatuAdmin)
admin.site.register(city, CityAdmin)
admin.site.register(info,InfoAdmin)
admin.site.register(price_delivery, PriceDeliveryAdmin)
admin.site.register(types_deliveries,TypesDeliveriesAdmin)
admin.site.register(schedules, SchedulesAdmin)
admin.site.register(types_client,TypesClientAdmin)
admin.site.register(lists_price,ListsPriceAdmin)
admin.site.register(inventory,InventoryAdmin)
admin.site.register(lists_client,ListsClientAdmin)
admin.site.register(category_shop,CategoryShopAdmin)
admin.site.register(category,CategoryAdmin)
admin.site.register(documents, DocumentShopAdmin)
admin.site.register(status_extend, statusExtendAdmin)
admin.site.register(method_payment, methodPaymentAdmin)
admin.site.register(shop_method_payment, shopMethodPaymentAdmin)
