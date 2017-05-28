from .views import *
from django.conf.urls import url

'''
#Users Module
router.register(r'users/info', UsersViewsets)
router.register(r'users/status', StatusViewsets)
#router.register(r'users/types', TypesViewsets)
router.register(r'users/devices', DevicesViewsets)
#router.register(r'users/notify', WithoutShopsViewsets)
#router.register(r'users/address', AddressViewsets)

'''
urlpatterns = [
	url(r'profile/update/', profileUpdate),
	url(r'profile/(?P<pk>[0-9]+)/$', profile),
	url(r'send/email/password/',sendEmailPassword),
	url(r'confirmAccount/',confirmAccount),
	url(r'xaddress/add/',addressAdd),
	url(r'(?P<pk>[0-9]+)/address/all/',allAddressUsers),
	url(r'address/all/',getAddress),
	url(r'deviceids/create/',deviceusers),
	url(r'add/',preRegisterUsers),
	url(r'super/rol/',AdminAddUsers),
	url(r'activate/',activateUsers),
	url(r'change/password/', changeEmailPassword),
	url(r'delete/', del_user),
	url(r'status/', suspendActivateUser),
	url(r'all/', allUsers),
	url(r'(?P<pk>[0-9]+)/products/sold/', mostSoldUser),
	#url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
	#	PasswordResetConfirmView.as_view(), 
	#	name='reset_password_confirm'),
	#url(r'^account/reset_password',ResetPasswordRequestView.as_view(), name="reset_password"),
	#url(r'^/password/reset/$', 'django.contrib.auth.views.password_reset', {'post_reset_redirect' : '/user/password/reset/done/'},name="password_reset"),
	#url(r'^/password/reset/done/$',
	#	'django.contrib.auth.views.password_reset_done'),
	#url(r'^/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
	#	'django.contrib.auth.views.password_reset_confirm', 
	#	{'post_reset_redirect' : '/user/password/done/'}),
	#url(r'^/password/done/$', 
	#	'django.contrib.auth.views.password_reset_complete'),
]
