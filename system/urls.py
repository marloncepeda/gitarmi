from .views import *
from django.conf.urls import url

urlpatterns = [
        url(r'terms/', terms),
	url(r'contact/phones/', getPhones),
	url(r'call/user/', requestingCallUser),
]

