from django.contrib import admin
from .models import *
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description','picture','class_icon', )

class SubcategoryAdmin(admin.ModelAdmin):
    search_fields = ('category_id__name', 'name','description',)
    list_display = ('category', 'name','description', )

class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name', 'sku','description',)
    list_display = ('name', 'sku','description','status','suggested_price','picture',)

'''
class category(models.Model):
class subcategory(models.Model):
class product(models.Model):
'''

admin.site.register(category, CategoryAdmin)
admin.site.register(subcategory, SubcategoryAdmin)
admin.site.register(product, ProductAdmin)
