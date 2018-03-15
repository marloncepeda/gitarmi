from .views import *
from django.conf.urls import url

urlpatterns = [
	url(r'change/availability/', changeAvailability),
]
