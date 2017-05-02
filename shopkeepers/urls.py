from .views import *
from django.conf.urls import url

urlpatterns = [
	url(r'(?P<pk>[0-9]+)/info/', getInfo),
	url(r'info/', Info),
	#url(r'(?P<pk>[0-9]+)/info/', getInfo),
	url(r'register/pre/',preRegister),
	url(r'(?P<pk>[0-9]+)/inventory/', inventories),
	url(r'list/', lists),
	url(r'geo/', geo),
	url(r'availability/', stateShop),
	url(r'settings/', infoUpdate),
	url(r'search/products/shop/', searchProductsShop),
	url(r'search/products/', searchProductsGeo),
	#url(r'settings/', shopProfile),
	url(r'(?P<pk>[0-9]+)/schedules/lists/', schedulesList),
	url(r'schedules/lists/add/', schedulesListAdd),
	url(r'inventory/add/product/', addProductInventory),
	url(r'inventory/change/product/', changeProductPrice),
	url(r'inventory/enable/product/', updateProductInventory),
	#url(r'(?P<pk>[0-9]+)/inventory/category/(?P<pk_cat>[0-9]+)/',getInventoriesxCategory),
	#url(r'(?P<pk>[0-9]+)/inventory/category/(?P<pk_cat>[0-9]+)/subcategory/(?P<pk_subc>[0-9]+)/',getInventoriesxCategoryxSubcategory),
	url(r'add/', addShop),
	url(r'summary/daily/shop/(?P<pk>[0-9]+)/',summaryDailyShop),
	url(r'summary/daily/',summaryDailyShops),
	url(r'category/all/',categoryShopOpen),
	url(r'search/shops/city/(?P<pk>[0-9]+)/', searchShopInCitiesId),
	url(r'all/',allShop),
	url(r'category/search/',searchCategoryShopOpen),
	url(r'products/(?P<pk>[0-9]+)/sold/', mostSoldShop),
	url(r'products/sold/globally/history/',mostSoldGloballyHistory),
	url(r'products/sold/globally/',mostSoldGlobally),
	url(r'cities/search/', searchCitiesName),
	url(r'search/shop/city/name/', searchShopInCitiesName),
	url(r'search/state/', searchShopState),
	url(r'search/',searchShopName),
	url(r'cities/', getCities),
	url(r'categories/', getShopCategories),
]
'''
	#url(r'^v2/users/',csrf_exempt(views.UserList.as_view())),
   
'''
