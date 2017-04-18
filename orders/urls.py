from .views import *
from django.conf.urls import url

urlpatterns = [
	url(r'user/(?P<pk>[0-9]+)/send/', orderUsersSend),
	url(r'user/(?P<pk>[0-9]+)/active/',orderUsersActive),
	url(r'user/(?P<pk>[0-9]+)/confirm/', orderUsersConfirm),
	url(r'user/(?P<pk>[0-9]+)/reject/', orderUsersReject),
	url(r'user/(?P<pk>[0-9]+)/end/', orderUsersEnd),
	url(r'ultimate/shop/(?P<pk>[0-9]+)/', ultimateFiveOrdersShop),
	url(r'ultimate/super/',ultimateOrders),
	url(r'support/ticket/(?P<pk>[0-9]+)/all/list/', ticketListShop),
	url(r'support/ticket/all/list/', ticketList),
	url(r'all/status/', ordersListStatus),
	url(r'all/super/', ordersListGlobal),
	url(r'all/', orders_list),
	url(r'statistics/orders/active/', ordersListDateActive),
	url(r'statistics/', ordersListDate),
	url(r'(?P<pk>[0-9]+)/detail/', order_detail),
	url(r'pedido/', pedido),
	url(r'confirmed/', orderConfirmed),
	url(r'rejected/', orderRejected),
	url(r'end/', orderEnd),
	url(r'search/', searchOrderId),
	#url(r'user/(?P<pk>[0-9]+)/send/', orderUsersSend),
	#url(r'support/ticket/all/list/', ticketList),
	#url(r'support/ticket/(?P<pk>[0-9]+)/all/list/', ticketListShop)
]
