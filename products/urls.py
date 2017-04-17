from .views import *
from django.conf.urls import url
urlpatterns = [
	url(r'all/list/', getProductsAllList),
	#url(r'category/(?P<pk>[0-9]+)/', getCategoryOneToOne ),
	url(r'category/(?P<pk>[0-9]+)/products/',getProductsAllCategory),
	url(r'category/(?P<pk>[0-9]+)/subcategory/', getSubcategoryOneToOne ),
	url(r'category/', getCategoryAll),
	url(r'subcategory/(?P<pk>[0-9]+)/products/', getProductsAll),
	url(r'subcategory/', getSubategoryAll),
	url(r'add/', addProduct),
	url(r'status/change/', suspendActivateProduct),
	url(r'/change/', editProductGlobal),
	#url(r'category/(?P<pk>[0-9]+)/subcategory/', getSubcategoryOneToOne ),
	#url(r'category/', category),
	#url(r'subcategory/', subcategory),
	#url(r'products/all/', productsAll),
	#url(r'category/all/', categoryAll),
	#url(r'subcategory/all/', subcategoryAll),
]
