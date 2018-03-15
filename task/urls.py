from .views import *
from django.conf.urls import url

urlpatterns = [
#	url(r'history/shop/', QualifyShopHistory),
#        url(r'history/user/', QualifyUserHistory),
#	url(r'user/', QualifyUser),
#	url(r'shop/', QualifyShop),
	url(r'create/',TaskCreate),
	url(r'activities/all/',ActivitiesAll),
	url(r'(?P<pk>[0-9]+)/info/', taskGetOne),
	url(r'all/pending/',TaskPendingAll),
	url(r'assign/',TaskAssign),
	url(r'changestatus/',TaskChangeStatus),
]
