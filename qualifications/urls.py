from .views import *
from django.conf.urls import url

urlpatterns = [
	url(r'user/', QualifyUser),
	url(r'shop/', QualifyShop),
	url(r'history/shop/', QualifyShopHistory),
	url(r'history/user/', QualifyUserHistory),
]