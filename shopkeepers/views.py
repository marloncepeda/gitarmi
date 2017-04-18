from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from .models import *
from .serializers import *
from orders.models import extended_order
from orders.serializers import *
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.measure import D, Distance
from django.contrib.gis.gdal import SpatialReference, CoordTransform
from django.contrib.gis.geos import Point
from orders.models import status, Orders
from orders.serializers import StatusSerializersBasic
from django.core.serializers.json import DjangoJSONEncoder
from push_notifications.gcm import gcm_send_message
from push_notifications.models import GCMDevice
from rest_framework_tracking.mixins import LoggingMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum,Count,Max
import json
from datetime import date, time
import datetime
from django.db.models import F

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addShop(request):
        if request.method == 'POST':
		data = json.loads(request.POST.get("data"))
                picture = request.FILES['picture']
		if(len(data["user"])==0)or(len(data["name"])==0)or(len(data["stratum"])==0):
                        JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
                else:
			newShop = info(user_id=int(data["user"]), name=data["name"], description =data["description"], phone=data["phone"], address=data["address"], picture=picture, type_shop_id = 1, status_verify_id=int(data["status_verify"]), rate=0, min_price=data["min_price"], average_deliveries=data["average_deliveries"], stratum=data["stratum"], min_shipping_price=data["min_shipping_price"], cat_shop=data["cat_shop"],poly='SRID=4326;POLYGON (('+data["polygon"]+'))')
                        newShop.save()
                        return JsonResponse({'petition':'OK','detail':'Shopkeeper created successfully'})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def geoDeprecated(request):
	if request.method == "POST":
		#order=json.loads(request.POST['point'])
		#point = order['lon'] + ' ' + order['lat']
		data = json.loads(request.body)
		point = data["point"]
		shop = info.objects.filter(poly__contains= GEOSGeometry("POINT("+ point +")"))
		serializer = InfoShopMinSerializers(shop, many=True)
		return Response(serializer.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def geo(request):
        if request.method == "POST":
                data = json.loads(request.body)
                point = data["point"]
		date = datetime.datetime.now().strftime("%Y-%m-%d")
              	
		states = state.objects.all().order_by('shopkeeper', '-date_register').distinct('shopkeeper').values('shopkeeper','state')
		stateList = json.dumps(list(states), cls=DjangoJSONEncoder)
		stateJson =json.loads(stateList)
		stateOpens = []

		for x in stateJson:
			if x["state"]=="Open":
				stateOpens.append(x["shopkeeper"])
			
		if (len(stateOpens)==0):
			return JsonResponse({'petition':'EMPTY','detail':'There are no open stores in the area'})
		else:
			shop = info.objects.filter(pk__in=stateOpens, poly__contains= GEOSGeometry("POINT("+ point +")"))	
			if (len(shop)==0):
				return JsonResponse({'petition':'DENY','detail':'There are no stores in the area'})
			else:
				serializer = InfoShopMinSerializers(shop, many=True)
				return Response(serializer.data)

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.IsAuthenticated,))
def Info(request):
	if request.method == 'POST':
		#Date Shopkeeper Info
		profile = info.objects.all().filter(user=request.POST.get("shop_id"))
		deviceids = request.POST.get("shop_deviceid")
		if deviceids:
			print 'existe la var deviceids'
		else:
			deviceids='online'
		try:
			gcm =GCMDevice.objects.get(registration_id=deviceids)
			gcm.save()
		except GCMDevice.DoesNotExist:
			gcm = GCMDevice(registration_id=deviceids,user=profile[0].user,name=profile[0].name)
			gcm.save()
		serializerInfo = InfoShopSerializers(profile, many=True)
		#Date State	
		states = state.objects.all().filter(shopkeeper=request.POST.get("shop_id")).order_by('-pk')[:1]
		serializerState = StateSerializersBasic(states, many=True)
		#Date Config Status Order
		statusOrder = status.objects.all().filter(shop=1)#cambiar a que agarre automatico el grupo de estados
		serializerStatusOrder = StatusSerializersBasic(statusOrder, many=True)
	
		statusOrders = []
		statusOrders.append({'orders_status':serializerStatusOrder.data})
		
		return Response(serializerInfo.data + serializerState.data + statusOrders)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def shopProfile(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		shopId = data["shop_id"]
		profile = info.objects.all().filter(pk=shopId)
		serializerInfo = InfoShopMinSerializers(profile, many=True)
		return Response(serializerInfo.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def allShop(request):
        if request.method == 'GET':
                #data = json.loads(request.body)
                #shopId = data["shop_id"]
                profile = info.objects.all()
                serializerInfo = InfoShopMinSerializers(profile, many=True)
                return Response(serializerInfo.data)

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.AllowAny,))
def infoUpdate(request):
	if request.method == 'POST':
		#Date Shopkeeper Info
		data = json.loads(request.POST['data'])
	
		nameShop = data[0]["shop_name"]
		minPrice = data[0]["shop_min_price"]
		shopId = data[0]["shop_id"]
		phoneShop = data[0]["shop_phone"]
		deliveryPrice = data[0]["shop_delivery_price"]
		infoShop = info.objects.all().filter(pk=shopId)
		
		if(len(infoShop)==0):
			return JsonResponse({'petition':'DENY','detail':'La tienda no existe'})
		else:
			infoShop.update(name = nameShop)
			infoShop.update(min_price = minPrice)
			infoShop.update(phone = phoneShop)
			infoShop.update(min_shipping_price = deliveryPrice)
		
			return JsonResponse({'petition':'OK','detail':'Shop updated successfully'})
		'''if (len(nameShop)==0) and (len(phoneShop)==0): 
			infoShop.update(min_price = minPrice)
			return JsonResponse({'detail':'Precio minimo de la tienda actualizado con exito'})
		elif (len(minPrice)==0) and (len(phoneShop)==0): 
			infoShop.update(name = nameShop)
		elif (len(minPrice)==0) and (len(nameShop)==0): 
			infoShop.update(phone = phoneShop)
			return JsonResponse({'detail':'Nombre de la tienda actualizado con exito'})
		elif (len(nameShop)==0) and (len(minPrice)==0) and (len(phoneShop)==0): 
			return JsonResponse({'detail':'tus variables estan vacias, intenta nuevamente enviando datos'})
		else:
			infoShop.update(name=nameShop, min_price=minPrice, phone= phoneShop)
			return JsonResponse({'detail':'Actualiado con exito'})'''
		#return JsonResponse({'petition':'OK','detail':'Actualiado con exito'})

@api_view(['GET','POST'])
@permission_classes((permissions.AllowAny,))
def stateShop(request):
	if request.method== 'POST':	
		if request.POST.get("shop_status") == '1':
			newState = state(
				shopkeeper_id=request.POST.get("shop_id"),
				state='Open'
			).save()
			return JsonResponse({'detail':'Cambio de estado a Open' })
		elif request.POST.get("shop_status") == '2':
			newState = state(
				shopkeeper_id=request.POST.get("shop_id"),
				state='Close'
			).save()
			return JsonResponse({'detail':'Cambio de estado a Close' })
		else: 
			return JsonResponse({'detail':'The shop_status field can not be empty'})

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.AllowAny,))
def inventories(request, pk):
	if request.method == 'GET':
		inventoriesS = inventory.objects.all().filter(shop_id=pk, enable=True)
		serializer = InventorySerializers(inventoriesS, many=True)
		return Response(serializer.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addProductInventory(request):
        if request.method == 'POST':
		shopid = request.POST.get("shop_id")
		productid = request.POST.get("shop_inv_productid")
		productprice = request.POST.get("shop_inv_price")

	        if(len(productprice)==0)or(len(productid)==0)or(len(shopid)==0):
			JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
		else:
			inventoriesS = inventory(shop_id=shopid,product_id=productid,enable=bool(True),base_price=productprice)
			inventoriesS.save()
			return JsonResponse({'petition':'OK','detail':'Created product'})
			
			'''try:
				inventory.objects.all().filter(shop_id=shopid,product_id=productid)
				return JsonResponse({'petition':'DENY','detail':'Duplicated product'})
			except:        
				inventoriesS = inventory(shop_id=shopid,product_id=productid,enable=bool(True),base_price=productprice)
                		inventoriesS.save()
               			return JsonResponse({'petition':'OK','detail':'Created product'})'''

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def changeProductPrice(request):
        if request.method == 'POST':
                shopid = request.POST.get("shop_id")
                productid = request.POST.get("shop_inv_productid")
                productprice = request.POST.get("shop_inv_price")

                if(len(productprice)==0)or(len(productid)==0)or(len(shopid)==0):
                        JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
                else:
			inventoriesS = inventory.objects.all().filter(shop=shopid,pk=productid)
                        inventoriesS.update(base_price=productprice)
			return JsonResponse({'petition':'OK','detail':'The product price changed to ' + productprice})

                        '''inventoriesS = inventory(shop_id=shopid,product_id=productid,enable=bool(True),base_price=productprice)
                        inventoriesS.save()
                        return JsonResponse({'petition':'OK','detail':'Created product'})'''

                        '''try:
                                inventory.objects.all().filter(shop=shopid,pk=productid,base_price=productprice)
                                return JsonResponse({'petition':'DENY','detail':'The product already has that price'})
                        except:        
                                inventoriesS = inventory.objects.all().filter(shop=shopid,pk=productid)
                                inventoriesS.update(base_price=productprice)

                                return JsonResponse({'petition':'OK','detail':'The product price changed to ' + productid})'''

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def updateProductInventory(request):
	if request.method == 'POST':
		shopid = request.POST.get("shop_id")
		productid = request.POST.get("shop_inv_productid")
		status = request.POST.get("shop_inv_prod_status")
		if (status=='TRUE')or(status=='true')or(status=='True'):
			statusc = True
		elif(status=='FALSE')or(status=='false')or(status=='False'):
			statusc = False
		
		if(len(status)==0)or(len(productid)==0)or(len(shopid)==0):
			JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
		else:
			inventoriesS = inventory.objects.all().filter(shop=shopid,pk=productid)
			inventoriesS.update(enable=bool(statusc))
			return JsonResponse({'petition':'OK','detail':'changed status product: '+ str(statusc)})

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getInventoriesxCategory(request, pk, pk_cat):
	if request.method == 'GET':
		inventoriesS = inventory.objects.all().filter(shop_id=pk,product__subcategory__category=pk_cat)
		serializer = InventorySerializers(inventoriesS, many=True)
		return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getInventoriesxCategoryxSubcategory(request, pk, pk_cat,pk_subc):
        if request.method == 'GET':
                inventoriesS = inventory.objects.all().filter(shop_id=pk,product__subcategory__category=pk_cat,product__subcategory=pk_subc)
                serializer = InventorySerializers(inventoriesS, many=True)
                return Response(serializer.data)
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def lists(request):
	if request.method == "GET":
		shop = info.objects.all()
		serializer = InfoShopMinSerializers(shop, many=True)
		return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def schedulesList(request,pk):
	if request.method == "GET":
		schedulesShop = schedules.objects.all().filter(shop_id=pk)
		if(len(schedulesShop)==0): 
			return JsonResponse([{'Petition':'EMPTY','message':'La tienda no tiene horarios',}])
		else:
			serializer = SchedulesSerializers(schedulesShop, many=True)
			return Response(serializer.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def schedulesListAdd(request):
	if request.method == "POST":
		schedules=json.loads(request.POST['data'])
		return HttpResponse(request.POST['data'])
		'''
		schedulesShop = schedules.objects.all().filter(shop_id=)
		if(len(schedulesShop)==0): 
			return JsonResponse([{'Petition':'EMPTY','message':'La tienda no tiene horarios',}])
		else:
			serializer = SchedulesSerializers(schedulesShop, many=True)
			return Response(serializer.data)
		'''

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def searchProductsGeo(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		point = data["point"]
		if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})

		if(data["extra"]=='True'):
			shop = inventory.objects.all().filter(shop__poly__contains= GEOSGeometry("POINT("+ point +")") ,product__name__unaccent__icontains=data["search"],enable=True)
                      	serializer = InventorySerializersFullwithShop(shop, many=True)
                       	if (len(shop)>0):
				return Response(serializer.data)
			else:
				return Response({'petition':'OK','detail':'The products you are looking for do not exist'})
		elif(data["extra"]=='False'):
			shop = inventory.objects.all().filter(shop__poly__contains= GEOSGeometry("POINT("+ point +")") ,product__name__unaccent__icontains=data["search"],enable=True)
			serializer = InventorySerializersFull(shop, many=True)
			if len(shop)>0:	
				return Response(serializer.data)
			else:
				return Response({'petition':'DENY','detail':'The products you are looking for do not exist'})
		else:
			return JsonResponse({'petition':'DENY','detail':'the fields extra dont have data'})
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def searchProductsShop(request):
        if request.method == "POST":
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
		elif(len(data["shop_id"])==0):
			return Response({'petition':'EMTPY','detail':'The fields shop_id not null'})
                try:
                        shop = inventory.objects.all().filter(shop_id=data["shop_id"],product__name__unaccent__icontains=data["search"],enable=True)
                        serializer = InventorySerializersFull(shop, many=True)
                        if (len(shop)>0):
                                return Response(serializer.data)
                        else:
                                return Response({'petition':'OK','detail':'The products you are looking for do not exist'})
                except:
                        return JsonResponse({'petition':'DENY','detail':'the fields extra dont have data'})

def server_error(request):
	context = {'foo': 'bar'}
	return render(request, '500.html', context)

def page_not_found(request):
	context = {'foo': 'bar'}
	return render(request, '404.html', context)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def summaryDailyShop(request):
	if request.method == "GET":
		date =datetime.datetime.now().strftime("%Y-%m-%d")
		shopOpens =state.objects.filter(state='Open',date_register__contains= date).values('shopkeeper_id').annotate(dcount=Count('shopkeeper_id'))
		sales =Orders.objects.filter(date_register__contains= date).aggregate(Sum('total')).get('total__sum')
		pedidos = Orders.objects.filter(date_register__contains= date).aggregate(Count('id')).get('id__count')
		newUsers = 0
		summaryDaily = []
                summaryDaily.append({'petition':'OK','shops_open':len(shopOpens),'total_sales':sales, 'total_orders':pedidos,'total_new_users':newUsers})
		return JsonResponse(summaryDaily,safe=False)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def categoryShopOpen(request):
        try:
		point = request.POST.get("point")
                date =datetime.datetime.now().strftime("%Y-%m-%d")
                shopOpens = state.objects.filter(state='Open',date_register__contains=date,shopkeeper__poly__contains=GEOSGeometry("POINT("+ point +")")).values('shopkeeper__cat_shop').annotate(total=Count('shopkeeper__cat_shop'))
                if(len(shopOpens)==0):
                        return JsonResponse({'petition':'EMPTY','detail':'There are no open stores in your area with the category to search'})
                else:
                        return Response(shopOpens)
        #except shopOpens.DoesNotExist:
        #       return JsonResponse({"petition":"DENY","detail":"Category"+category+"does not exist"})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def searchCategoryShopOpen(request):
       	try:
		category = request.POST.get("category")
		point = request.POST.get("point")
                date =datetime.datetime.now().strftime("%Y-%m-%d")
                shopOpens = state.objects.filter(state='Open',date_register__contains=date,shopkeeper__cat_shop__unaccent__icontains=category, shopkeeper__poly__contains=GEOSGeometry("POINT("+ point +")")).values('shopkeeper__cat_shop','shopkeeper_id','shopkeeper__name','shopkeeper__min_price','shopkeeper__phone','shopkeeper__picture','shopkeeper__rate','shopkeeper__average_deliveries','shopkeeper__min_shipping_price','shopkeeper__stratum').annotate(total=Count('shopkeeper__cat_shop'))
               	if(len(shopOpens)==0):
			return JsonResponse({'petition':'EMPTY','detail':'There are no open stores in your area'})
		else:
			return Response(shopOpens)
	#except shopOpens.DoesNotExist:
        #	return JsonResponse({"petition":"DENY","detail":"Category"+category+"does not exist"})
    	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def mostSoldGlobally(request):
        try:
                mostSold = extended_order.objects.all().annotate(image=F('product__product__picture'),price=F('product__base_price'),suggested_price=F('product__product__suggested_price'),name=F('product__product__name'),description=F('product__product__description')).values('product_id','image','price','suggested_price','name','description').annotate(total=Count('product_id')).order_by('-total')[:10]
                if(len(mostSold)==0):
                        return JsonResponse({'petition':'EMPTY','detail':'There are no products to calculate the best sellers'})
                if(len(mostSold)==0):
                        return JsonResponse({'petition':'EMPTY','detail':'There are no products to calculate the best sellers'})
                else:
                        return Response(mostSold)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def mostSoldGloballyHistory(request):
        try:
                mostSold = extended_order.objects.all().annotate(image=F('product__product__picture'),price=F('product__base_price'),suggested_price=F('product__product__suggested_price'),name=F('product__product__name'),description=F('product__product__description')).values('product_id','image','price','suggested_price','name','description').annotate(total=Count('product_id')).order_by('-total')
                if(len(mostSold)==0):
                        return JsonResponse({'petition':'EMPTY','detail':'There are no products to calculate the best sellers'})
                else:
                        return Response(mostSold)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchShopName(request):
        try:
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                shop = info.objects.all().filter(name__unaccent__icontains=data["search"])
                serializer = InfoShopSerializers(shop, many=True)
                if (len(shop)>0):
                	return Response(serializer.data)
                else:
                	return Response({'petition':'OK','detail':'The shop you are looking for do not exist'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The shop does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getCities(request):
        try:
                cities = city.objects.all()
                serializer = cityAllSerializers(cities, many=True)
                if (len(cities)>0):
                        return Response(serializer.data)
                else:
                        return Response({'petition':'OK','detail':'There are no cities currently registered'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"There are no cities currently registered"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})



