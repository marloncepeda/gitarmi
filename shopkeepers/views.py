from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from .models import *
from users.models import Profile
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
from django.core import serializers
from django.core.paginator import Paginator
from django.contrib.auth.models import User

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def preRegister(request):
        try:
                data = json.loads(request.body)#json.loads(request.POST.get("data"))
                if(len(data["email"])==0)or(len(data["name"])==0)or(len(data["stratum"])==0):
                        JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
                else:
			new_user = User.objects.create_user(data["email"],data["email"],data["password"])
                        new_user.is_active = False
                        new_user.first_name = data["name"]
                        new_user.save()
                        profile_user = Profile(user_id=new_user.id,phone=data["phone"],type_user_id=2, birthdate=data["birthdate"],status_id=2)
                        profile_user.save()

                        newShop = info(user_id=new_user.id, name=data["name_shop"],city_id=data["city_shop"],min_price=0,min_shipping_price=0,phone=data["phone"], stratum=data["stratum"], cat_shop=data["cat_shop"], address=data["address_shop"], type_shop_id = 1, status_verify_id=2, rate=0,poly=None)#'SRID=4326;POLYGON( (0 0,1 1, 2 2, 0 0) )')
                        newShop.save()
                        status = status_extend(shop=newShop, status_id=4)
                        status.save()
			methodpay = shop_method_payment(shop_id=newShop.id,method_pay_id=1,status=True)
			methodpay.save()
                        states = state(shopkeeper_id=newShop.id,state="Close")
                        states.save()
                        return JsonResponse({'petition':'OK','detail':'Pre register created successfully'})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def addShop(request):
        try:
		data = json.loads(request.POST.get("data"))
                picture = request.FILES['picture']
		if(len(data["user"])==0)or(len(data["name"])==0)or(len(data["stratum"])==0):
                        JsonResponse({'petition':'DENY','detail':'The shop_(Fields) field can not be empty'})
                else:
			newShop = info(user_id=int(data["user"]), name=data["name"], description =data["description"], phone=data["phone"], address=data["address"], picture=picture, type_shop_id = 1, status_verify_id=4, rate=0, min_price=data["min_price"], average_deliveries=data["average_deliveries"], stratum=data["stratum"], min_shipping_price=data["min_shipping_price"], cat_shop=data["cat_shop"],city_id=data["city_id"],poly='SRID=4326;POLYGON (('+data["polygon"]+'))')
                        newShop.save()
			status = status_extend(shop=newShop, status_id=4)
			status.save()
			states = state(shopkeeper_id=newShop.id,state="Close")
			states.save()
			methodpay =  shop_method_payment(shop_id=newShop.id,method_pay_id=1,status=True)
                        methodpay.save()
                        return JsonResponse({'petition':'OK','detail':'Shopkeeper created successfully'})
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

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
        try:
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
				
				for shop in serializer.data:
					methodPay = shop_method_payment.objects.filter(shop_id=shop["id"], status=True)
					
					if len(methodPay)==0:
						pass
					else:
						serializer1 = ShopMethodPaymentSerializers(methodPay, many=True)
						shop["methods_payment"]=serializer1.data
						#return JsonResponse(serializer.data,safe=False)#shop1[0].method_pay.name,safe=False)
			
				return Response(serializer.data)
	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def Info(request):
	try:
		#Date Shopkeeper Info
		profile = info.objects.all().filter(user=request.POST.get("shop_id"))
		deviceids = request.POST.get("shop_deviceid","online")
		gcm = GCMDevice.objects.all().filter(user=profile[0].user)

		if len(gcm)==0:
			gcm1 = GCMDevice(registration_id=deviceids,user=profile[0].user,name=profile[0].name)
			gcm1.save()
		else:
			gcm[0].registration_id=deviceids
			gcm[0].save()
		
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

	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def getInfo(request,pk):
        if request.method == 'GET':
                #Date Shopkeeper Info
                profile = info.objects.all().filter(pk=pk)
                serializerInfo = InfoShopSerializersPoly(profile, many=True)
                #Date State     
                states = state.objects.all().filter(shopkeeper_id=pk).order_by('-pk')[:1]
                serializerState = StateSerializersBasic(states, many=True)
             	
                return Response(serializerInfo.data + serializerState.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def shopProfile(request):
	if request.method == 'POST':
		data = json.loads(request.body)
		shopId = data["shop_id"]
		profile = info.objects.all().filter(pk=shopId)
		serializerInfo = InfoShopSerializers(profile, many=True)
		return Response(serializerInfo.data)
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def allShop(request):
        if request.method == 'GET':
                #data = json.loads(request.body)
                #shopId = data["shop_id"]
                profile = info.objects.all()
                serializerInfo = InfoShopMinSerializers(profile, many=True)
                return Response(serializerInfo.data)
'''
@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def allShop(request):
        if request.method == "POST":
                shop_offsets = request.POST.get("offset",30)
                shop_pages = request.POST.get("page",1)
                shop = info.objects.all()

		paginator = Paginator(shop, shop_offsets)
                shop_detail = paginator.page(shop_pages)
                serializer = InfoShopMinSerializers(shop_detail, many=True)
                Paginations = []
                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                return Response(serializer.data + Paginations)

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.AllowAny,))
def infoUpdate(request):
	if request.method == 'POST':
		#Date Shopkeeper Info
		data = json.loads(request.POST['data'])
		shopId = data[0]["shop_id"]
		infoShop = info.objects.all().filter(pk=shopId)
		fields= []
		nofields = []
	
		if len(infoShop)==0:
			return JsonResponse({'petition':'EMPTY','detail':'Does not exist shops with id: '+shopId})
		
		for updates in data:
			#return JsonResponse(updates["shop_id"] is not None ,safe=False)
			if updates["shop_name"] is not None:
				infoShop.update(name = updates["shop_name"])
				fields.append('shop_name')

			if updates["shop_min_price"] is not None:
				infoShop.update(min_price = updates["shop_min_price"])
				fields.append('shop_min_price')

			if updates["shop_phone"] is not None:
				infoShop.update(phone = updates["shop_phone"])
                                fields.append('shop_phone')

			if updates["shop_delivery_price"] is not None:
				infoShop.update(min_shipping_price = updates["shop_delivery_price"])
                                fields.append('shop_delivery_price')

			if updates["poly"] is not None:
				infoShop.update(poly ='SRID=4326;POLYGON( ('+ updates["poly"] +') )')
                                fields.append('poly')

			if updates["shop_id"] is not None:
				pass
			else:
				nofields.append({'NoFields':updates,'error':'the field does not exist in shopkeepers'})

		return JsonResponse({'petition':'OK','fields_update':fields,'detail':'Update the shopkeeper information'})#'no_fields_update':nofields,

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

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def inventories(request, pk):
	if request.method == 'GET':
		inventoriesS = inventory.objects.all().filter(shop_id=pk, enable=True)
		serializer = InventorySerializers(inventoriesS, many=True)
		return Response(serializer.data)
	if request.method == "POST":
		try:
                	shop_offsets = request.POST.get("offset",10)
                	shop_pages = request.POST.get("page",1)
			extra = request.POST.get("extra",False)
			if((extra=='True') or (extra=='true')):
				shop = inventory.objects.all().filter(shop_id=pk, product__status=True)
			else:
                		shop = inventory.objects.all().filter(shop_id=pk, enable=True,product__status=True)

                	paginator = Paginator(shop, shop_offsets)
                	shop_detail = paginator.page(shop_pages)
                	serializer = InventorySerializers(shop_detail, many=True)
                	Paginations = []
               		Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
			data = []
			data.append({'inventory':serializer.data,'pagination':Paginations})
                	return Response(data)

		except Exception as e:
                	return JsonResponse({"petition":"ERROR","detail":e.message})
	
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
		date =datetime.datetime.now().strftime("%Y-%m-%d")
		point = data["point"]
		if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})

		if(data["extra"]=='True'):
			shop = inventory.objects.all().filter(shop__poly__contains= GEOSGeometry("POINT("+ point +")") ,product__name__unaccent__icontains=data["search"],enable=True)
                      	serializer = InventorySerializersFullwithShop(shop, many=True)
                       	
			if (len(shop)>0):
				return JsonResponse(serializer.data, safe=False)
			else:
				return Response({'petition':'OK','detail':'The products you are looking for do not exist'})
		elif(data["extra"]=='False'):
			shop = inventory.objects.all().filter(shop__poly__contains= GEOSGeometry("POINT("+ point +")") ,product__name__unaccent__icontains=data["search"],enable=True)
			serializer = InventorySerializersFull(shop, many=True)
	
			'''data1 = json.dumps(serializer.data)
	                data2 = json.loads(data1)

			data3 = []
	
			for x in data2:
				stateShop = state.objects.filter(date_register__icontains=date).order_by("-pk")[:1]
				return Response(stateShop[0].state)
				if stateShop[0].state=="Open":
					return Response("si esta abierto"+x)'''
		
			if len(shop)>0:	
				return JsonResponse(serializer.data, safe=False)#data3,safe=False)
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
def summaryDailyShops(request):
	if request.method == "GET":
		date =datetime.datetime.now().strftime("%Y-%m-%d")
		shopOpens =state.objects.filter(state='Open',date_register__contains= date).values('shopkeeper_id').annotate(dcount=Count('shopkeeper_id'))
		#shopOpens2 =state.objects.all().filter(date_register__contains= date).order_by('-pk')
		#serializerState = StateSerializersFull(shopOpens2, many=True)
		#data = serializers.serialize('json', state.objects.all(), fields=('pk','shopkeeper_id','state','date_register'))
		#data2 = json.loads(data)
		#return JsonResponse(serializerState.data,safe=False)
		sales =Orders.objects.filter(date_register__contains= date).aggregate(Sum('total')).get('total__sum')
		pedidos = Orders.objects.filter(date_register__contains= date).aggregate(Count('id')).get('id__count')
		newUsers = User.objects.all().filter(date_joined__contains=date).aggregate(Count('id')).get('id__count')
		summaryDaily = []
                summaryDaily.append({'shops_open':len(shopOpens),'total_sales':sales, 'total_orders':pedidos,'total_new_users':newUsers})
		return JsonResponse(summaryDaily,safe=False)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def summaryDailyShop(request, pk):
	try:
                date =datetime.datetime.now().strftime("%Y-%m-%d")
                mostSold = extended_order.objects.filter(date_register__contains= date, order__shop_id=pk).annotate(image=F('product__product__picture'),price=F('product__base_price'),name=F('product__product__name')).values('product_id','image','price','name').annotate(total=Count('product_id')).order_by('-total')[:1]
                sales =Orders.objects.filter(date_register__contains= date, shop_id=pk).aggregate(Sum('total')).get('total__sum')
                pedidosRecibidos = Orders.objects.filter(date_register__contains= date, shop_id=pk, status_order__in=("1","2","3","4")).aggregate(Count('id')).get('id__count')
		pedidosTerminados = Orders.objects.filter(date_register__contains= date, shop_id=pk, status_order__in=("4")).aggregate(Count('id')).get('id__count')
		if sales is None:
			sales = 0
		if len(mostSold)==0:
			mostSold ="Nothing has been sold until the moment " + date
                summaryDaily = []
                summaryDaily.append({'total_sales':sales, 'total_orders':pedidosRecibidos,'total_end_orders':pedidosTerminados,'most_sold':mostSold})
                return Response(summaryDaily)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

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
                mostSold = extended_order.objects.all().annotate(image=F('product__product__picture'),price=F('product__base_price'),suggested_price=F('product__product__suggested_price'),name=F('product__product__name'),description=F('product__product__description')).values('product_id','image','price','suggested_price','name','description').annotate(total=Count('product_id')).order_by('-total')[:5]
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
def mostSoldShop(request,pk):
        try:
                mostSold = extended_order.objects.all().filter(order__shop_id=pk).annotate(image=F('product__product__picture'),price=F('product__base_price'),suggested_price=F('product__product__suggested_price'),name=F('product__product__name'),description=F('product__product__description')).values('product_id','image','price','suggested_price','name','description').annotate(total=Count('product_id')).order_by('-total')[:5]
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

		data = serializers.serialize('json', shop)
		data1 = json.dumps(serializer.data)
		data2 = json.loads(data1)

		for x in data2:
			states = state.objects.all().filter(shopkeeper=x["id"]).order_by('-pk')[:1]
			x.update({"state":states[0].state})
			
		if (len(shop)>0):
                	return JsonResponse(data2, safe=False)
                else:
                	return Response({'petition':'OK','detail':'The shop you are looking for do not exist'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The shop does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
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

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchCitiesName(request):
        try:
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                cities = city.objects.all().filter(name__unaccent__icontains=data["search"])
                serializer = cityAllSerializers(cities, many=True)
                if (len(cities)>0):
                        return Response(serializer.data)
                else:
                        return Response({'petition':'OK','detail':'The city you are looking for do not exist'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The city does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchShopInCitiesName(request):
        try:
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                shops = info.objects.all().filter(city__name__unaccent__icontains=data["search"])
                serializer = InfoShopSerializers(shops, many=True)
                if (len(shops)>0):
                        return Response(serializer.data)
                else:
                        return Response({'petition':'EMPTY','detail':'The city has no stores currently created'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The city does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def searchShopInCitiesId(request,pk):
        try:
                shops = info.objects.all().filter(city__pk=pk)
                serializer = InfoShopSerializers(shops, many=True)
                if (len(shops)>0):
                        return Response(serializer.data)
                else:
                        return Response({'petition':'EMPTY','detail':'The city has no stores currently created'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The city does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchShopState(request):
        try:
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                
		shop = info.objects.all().filter(status_verify__name__unaccent__icontains=data["search"])
                serializer = InfoShopSerializers(shop, many=True)
                
		data = serializers.serialize('json', shop)
                data1 = json.dumps(serializer.data)
                data2 = json.loads(data1)
		#return JsonResponse(data2, safe=False)
		#return getOnboarding('1',1)

                for x in data2:
			history = status_extend.objects.all().filter(shop=x["id"]).order_by('-pk')[:1]
                        states = state.objects.all().filter(shopkeeper=x["id"]).order_by('-pk')[:1]
			if history[0].status.name=="Suspendido":
				x.update({"status_verifys":{'id':history[0].id,'reason':history[0].reason,'name':history[0].status.name,'date_status_change':history[0].date_register}})
			else:
				x.update({"status_verifys":{'id':history[0].id,'name':history[0].status.name,'date_status_change':history[0].date_register}})
			x.update({'onboarding':{'cant_total':'6','approved':'2'}})
			x.update({"state":states[0].state})
			x.pop('status_verify')
		
                if (len(data2)>0):
                        return JsonResponse(data2, safe=False)
                else:
                        return Response({'petition':'OK','detail':'There are no stores with the state to look for, try with: [Activo,Leads,Suspendido,Revision]'})
        
	except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The status shop does not exist"})
	
	#except Exception as e:
        #        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getShopCategories(request):
        try:
                shops = info.objects.all().filter().values('cat_shop').annotate(total=Count('cat_shop'))          
                if (len(shops)>0):
                        return Response(shops)
                else:
                        return Response({'petition':'EMPTY','detail':'The city has no stores currently created'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The city does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

'''
Resumen de cuenta para onboarding
documento basico
documentos y perfil
aceptado y aprobado
un inventario
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getOnboarding(request, pk):
        try:
		
                shops = info.objects.all().filter(pk=pk)
		checkList = []
		
		if( (len(shops[0].phone)==0) or (len(shops[0].address)==0) or (len(shops[0].cat_shop)==0) or (len(shops[0].min_price)==0) ):
			checkList.append({'basic_register':False,'profile':False,'documents':False,'accept_active':False,'article_inventory':False})
			return Response(checkList)
		else:
			
			profile = Profile.objects.all().filter(user_id=shops[0].user.id)
			#return JsonResponse(profile,safe=False)
			if( (len(profile[0].phone)==0) ):
				profile_status=True
				checkList.append({'basic_register':[{'date_register':shops[0].date_register,'status':True}],'profile':False,'documents':False,'accept_active':False,'article_inventory':False})
				return Response(checkList)
			else:
				profile_status= True
                                profile_date= profile[0].date_register
		
			docs = documents.objects.all().filter(shop_id=pk)
			#if( (len(docs[0].cedula)==0) or (len(docs[0].camara_comercio)==0) or (len(docs[0].recibo_servicio)==0) or (len(docs[0].rut)==0)):
			if(len(docs)==0):
				checkList.append({'basic_register':[{'date_register':shops[0].date_register,'status':True}],'profile':[{'status':profile_status,'date_register':profile_date}],'documents':False,'accept_active':False,'article_inventory':False})
				return Response(checkList)
			else:
				docs_status= True
                                docs_date= docs[0].date_register
			
			if( (shops[0].status_verify.name == 'Suspendidos')or (shops[0].status_verify.name == 'Leads') or (shops[0].status_verify.name == 'Revision') ):
				checkList.append({'basic_register':[{'date_register':shops[0].date_register,'status':True}],'profile':[{'status':profile_status,'date_register':profile_date}],'documents':[{'status':docs_status,'date_register':docs_date}],'accept_active':False,'article_inventory':False})
				return Response(checkList)
			else:
				shop_status= True
                                shop_date= shops[0].date_register
			
			inventories = inventory.objects.all().filter(shop_id=pk).order_by('-pk')[:1]
			#return JsonResponse(inventories,safe=False)
			if(len(inventories)==0):
				checkList.append({'basic_register':[{'date_register':shops[0].date_register,'status':True}],'profile':[{'status':profile_status,'date_register':profile_date}],'documents':[{'status':docs_status,'date_register':docs_date}],'accept_active':[{'status':profile_status,'date_register':profile_date}],'article_inventory':False})
				return Response(checkList)		
			else:
				inv_status= True
                                inv_date= inventories[0].date_register
					
		checkList.append({'basic_register':[{'date_register':shops[0].date_register,'status':True}],'profile':[{'status':profile_status,'date_register':profile_date}],'documents':[{'status':docs_status,'date_register':docs_date}],'accept_active':[{'status':shop_status,'date_register':shop_date}],'article_inventory':[{'status':inv_status,'date_register':inv_date}]})
		return Response(checkList)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addDocuments(request):
        try:
		id = request.POST.get("shop_id")
                rut = request.FILES['rut']
		cc = request.FILES['cc']
		camara = request.FILES['camara']
		recibo = request.FILES['recibo']
		tipo_usuario = request.POST.get("tipo_usuario")
                if( (len(id)==0) or (len(rut)==0) or (len(camara)==0) or (len(cc)==0) or(len(recibo)==0) or (len(tipo_usuario)==0) ):
                        JsonResponse({'petition':'DENY','detail':'The field can not be empty'})
                else:
                        document = documents(shop_id=id,cedula=cc,rut=rut,camara_comercio=camara,recibo_servicio=recibo,type_client=tipo_usuario)
                        document.save()
                        return JsonResponse({'petition':'OK','detail':'Documents shopkeeper created successfully'})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getDocuments(request,pk):
	try:
		document = documents.objects.all().filter(shop_id=pk)
		serializer = DocumentsSerializers(document, many=True)
		return Response(serializer.data)		 	
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getOnboarding2(request, pk):
        try:
		checkList = []
                basicRegister = []
                profiles = []
                documentsShop = []
                acceptActive = []
                articleInventory = []		
		#Registro basico de tienda
                shops = info.objects.all().filter(pk=pk)
		if len(shops)==0:
			return JsonResponse({'petition':'DENY','detail':'the shop does not exist'})

		#return JsonResponse(shops[0].poly is None,safe=False)#="SRID=4326;LINEARRING (0 0, 1 1, 2 2, 0 0)" ,safe=False)
		if( (len(shops[0].phone)==0) or (len(shops[0].address)==0) or (len(shops[0].cat_shop)==0) or (len(shops[0].min_price)==0) or (shops[0].poly is None)):
			basicRegister.append(False)
		else:
			basicRegister.append({'date_register':shops[0].date_register,'status':True})
		
		#Perfil del tendero
		profile = Profile.objects.all().filter(user_id=shops[0].user.id)                   
                if( (len(profile[0].phone)==0) ):
			profiles.append(False)
                else:
			profiles.append({'status':True,'date_register':profile[0].date_register})
		
		#Documentos de la tienda y tendero
		docs = documents.objects.all().filter(shop_id=pk)
		if (len(docs)==0):
			documentsShop.append(False)
                else:
                        documentsShop.append({'status':True,'date_register':docs[0].date_register})
			
		#Verificar si a tienda esta aceptada o no
		if( (shops[0].status_verify.name == 'Suspendidos')or (shops[0].status_verify.name == 'Leads') or (shops[0].status_verify.name == 'Revision') ):
                        acceptActive.append(False)
                else:
                        acceptActive.append({'status':True,'date_register':shops[0].date_register})
		
		#Verificar si tiene articulos creados en su inventario
		inventories = inventory.objects.all().filter(shop_id=pk).order_by('-pk')[:1]
                if (len(inventories)==0):
                        articleInventory.append(False)
                else:
                        articleInventory.append({'status':True,'date_register':inventories[0].date_register})
	
			'''para validar docs luego
			if( (len(docs[0].cedula)==0) or (len(docs[0].camara_comercio)==0) or (len(docs[0].recibo_servicio)==0) or (len(docs[0].rut)==0)):'''
					
		checkList.append({'basic_register':basicRegister[0],'profile':profiles[0],'documents':documentsShop[0],'accept_active':acceptActive[0],'article_inventory':articleInventory[0] })
		return Response(checkList)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
