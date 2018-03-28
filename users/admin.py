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

class UsersProfileAdmin(admin.ModelAdmin):
    search_fields = ('user', 'phone','type_user','status',)
    list_display = ('first_name','last_name','user_email', 'phone','type_user','status','date_register', )

    def user_email(self, instance):
    	return instance.user.email

    def first_name(self, instance):
    	return instance.user.first_name

    def last_name(self, instance):
    	return instance.user.last_name

admin.site.register(Status,StatusAdmin)
admin.site.register(Types, UsersTypeAdmin)
admin.site.register(Profile,UsersProfileAdmin)
