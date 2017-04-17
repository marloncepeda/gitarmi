from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
# Register your models here.
class StatusAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description','date_register', )

class UsersTypeAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description','date_register', )

class AddressAdmin(admin.ModelAdmin):
    search_fields = ('address_alias','address',)
    list_display = ('client', 'address_alias','address','address_detail','lat','lon','date_register')

class UsersProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'phone','pictures','type_user','status',)
    list_display = ('first_name','last_name','user_email', 'phone','pictures','type_user','status','date_register', )

    def user_email(self, instance):
    	return instance.user.email

    def first_name(self, instance):
    	return instance.user.first_name

    def last_name(self, instance):
    	return instance.user.last_name

class TagsAdmin(admin.ModelAdmin):
    search_fields = ('name', 'description',)
    list_display = ('name', 'description','date_register', )

class UsersTagsAdmin(admin.ModelAdmin):
    search_fields = ('user', 'tag',)
    list_display = ('user', 'tag','date_register', )

admin.site.register(Status,StatusAdmin)
admin.site.register(Types, UsersTypeAdmin)
admin.site.register(Profile,UsersProfileAdmin)
admin.site.register(Address,AddressAdmin)
admin.site.register(tags,TagsAdmin)
admin.site.register(users_tags,UsersTagsAdmin)
