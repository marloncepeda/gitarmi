from django.contrib import admin
from .models import *

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name','address',)
    list_display = ('name','address','description','phone1','phone2','phone3','phone4','email','date_register')


class termsAndConditionsAdmin(admin.ModelAdmin):
    search_fields = ('version',)
    list_display = ('document', 'version','date_register')

admin.site.register(company,CompanyAdmin)
admin.site.register(termsAndConditions,termsAndConditionsAdmin)

