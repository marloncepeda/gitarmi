from django.contrib import admin
from .models import *

# Register your models here.
'''
class AddressAdmin(admin.ModelAdmin):
    search_fields = ('address_alias','address',)
    list_display = ('client', 'address_alias','address','address_detail','lat','lon','date_register')

admin.site.register(Address,AddressAdmin)
'''
