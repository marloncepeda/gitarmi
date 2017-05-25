from .views import *
from django.conf.urls import url

urlpatterns = [
	url(r'history/shop/', QualifyShopHistory),
        url(r'history/user/', QualifyUserHistory),
	url(r'user/', QualifyUser),
	url(r'shop/', QualifyShop),
]
