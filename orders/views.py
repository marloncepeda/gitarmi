from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from .models import *
from .serializers import *
from users.models import Profile
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from shopkeepers.models import info, inventory
from users.models import Address,Profile
from shopkeepers.models import info
from push_notifications.gcm import gcm_send_message
from push_notifications.models import GCMDevice
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Avg
import datetime
from django.db.models import Sum,Max
import json
from django.core import serializers
#from emitter import Emitter
from socketIO_client import SocketIO, LoggingNamespace

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ticketList(request):
	if request.method == "GET":
		shop = ticket_support.objects
		serializer = ticketSupportSerializers(shop, many=True)
		return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ticketListShop(request,pk):
        if request.method == "GET":
		shop_offsets = request.GET.get("offset",10)
                shop_pages = request.GET.get("page",1)
		ticket_status = request.GET.get("status",1)
                shop = ticket_support.objects.all().filter(status_id__in=[ticket_status],order__shop_id=pk).order_by('-pk')
		if(len(shop)==0):
			return JsonResponse({'petition':'EMPTY','detail':'The shop dont have ticket'})
		else:
			if (shop_offsets==30):
                                serializer = ticketSupportSerializers(shop, many=True)
                                return Response(serializer.data)
                        else:
                                paginator = Paginator(shop, shop_offsets)
                                shop_detail = paginator.page(shop_pages)
                                serializer = ticketSupportSerializers(shop_detail, many=True)
                                Paginations = []
                                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                                return Response(serializer.data + Paginations)
                	#serializer = ticketSupportSerializers(shop, many=True)
			#return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ticketUltimatePending(request):
        if request.method == "GET":
                pending = ticket_support.objects.all().filter(status_id__in=[1,3])[:5]
		close = ticket_support.objects.all().filter(status_id=2)[:5]
              
                serializer = ticketSupportSerializers(pending, many=True)
                serializers = ticketSupportSerializers(close, many=True)
		data = []
		data.append({'pending':serializer.data, 'close':serializers.data})
		return Response(data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ticketAllShopList(request):
        if request.method == "GET":
                shop_offsets = request.GET.get("offset",10)
                shop_pages = request.GET.get("page",1)
		ticket_status = request.GET.get("status",1)
                shop = ticket_support.objects.all().filter(status_id__in=[ticket_status]).order_by('-date_register')

                paginator = Paginator(shop, shop_offsets)
                shop_detail = paginator.page(shop_pages)
                serializer = ticketSupportSerializers(shop_detail, many=True)
                Paginations = []
                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                data=[]
		data.append({'pagination':Paginations,'tickets':serializer.data})
		return Response(data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def ultimateOrders(request):
	if request.method == "GET":
		orders = Orders.objects.all().filter().order_by('-date_register')[:5]
		serializer = OrderSerializerWithShop(orders, many=True)
		data1 = json.dumps(serializer.data)
                data2 = json.loads(data1)

                for x in data2:
			phone = Profile.objects.all().filter(user_id=x['user']['id'])
			if len(phone)==0:
                                x['user'].update({"phone":"null"})
                        else:
                                x['user'].update({"phone":phone[0].phone})
			
		return Response(data2)

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def ordersListGlobal(request):
	if request.method == "POST":
		shop_id = request.POST.get("shop_id")
		shop_offsets = request.POST.get("offset",10)
		shop_pages = request.POST.get("page",1)
		if(len(shop_id)==0): 
			return JsonResponse({'detail':'The shop field can not be empty'})
		else:
			shop = Orders.objects.all().filter().order_by('-date_register')
			
			paginator = Paginator(shop, shop_offsets)
			shop_detail = paginator.page(shop_pages)
			serializer = OrderSerializerWithShop(shop_detail, many=True)
			data1 = json.dumps(serializer.data)
                	data2 = json.loads(data1)

                	for x in data2:
                        	phone = Profile.objects.all().filter(user_id=x['user']['id'])
                        	if len(phone)==0:
                                	x['user'].update({"phone":"null"})
                        	else:
                                	x['user'].update({"phone":phone[0].phone})

			Paginations = []
			Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
			return Response(data2 + Paginations)

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def orders_list(request):
        if request.method == "POST":
                shop_id = request.POST.get("shop_id")
                shop_offsets = request.POST.get("offset",30)
                shop_pages = request.POST.get("page",1)
                if(len(shop_id)==0):
                        return JsonResponse({'detail':'The shop field can not be empty'})
                else:
                        shop = Orders.objects.all().filter(shop=shop_id).order_by('-pk')
                        if (shop_offsets==30):
                                serializer = OrderSerializerBasic(shop, many=True)
                                return Response(serializer.data)
                        else:
                                paginator = Paginator(shop, shop_offsets)
                                shop_detail = paginator.page(shop_pages)
                                serializer = OrderSerializerWithShop(shop_detail, many=True)
                                Paginations = []
                                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                                return Response(serializer.data + Paginations)

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def ordersListStatus(request):
        try:
                shop_id = request.POST.get("shop_id")
                shop_offsets = request.POST.get("offset",30)
                shop_pages = request.POST.get("page",1)
		order_statusId = request.POST.get("order_status_ids")
		
		if shop_id is None:
                        return JsonResponse({'detail':'The shop field can not be empty'})
                else:
			
                        shop = Orders.objects.all().filter(shop=shop_id,status_order__in=(order_statusId[0], order_statusId[2], order_statusId[4], order_statusId[6])).order_by('-pk')
			if (shop_offsets==30):
				serializer = OrderSerializerBasic(shop, many=True)
				return Response(serializer.data)
                       	else:
                                paginator = Paginator(shop, shop_offsets)
                                shop_detail = paginator.page(shop_pages)
                                serializer = OrderSerializerBasic(shop_detail, many=True)
				Paginations = []
                                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                                return Response(serializer.data + Paginations)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def ordersListStatusUsers(request):
        try:
                user_id = request.POST.get("user_id")
                offsets = request.POST.get("offset",30)
                pages = request.POST.get("page",1)
                order_statusId = request.POST.get("order_status_ids")

                if user_id is None:
                        return JsonResponse({'detail':'The user_id field can not be empty'})
                else:

                        shop = Orders.objects.all().filter(user_id=user_id,status_order__in=(order_statusId[0], order_statusId[2], order_statusId[4], order_statusId[6])).order_by('-pk')
                        paginator = Paginator(shop, offsets)
                        user_detail = paginator.page(pages)
                        serializer = OrderSerializerUsers(user_detail, many=True)
                        Paginations = []
                        Paginations.append({'num_pages':paginator.num_pages,'actual_page':pages})
			data = []
			data.append({'pagination':Paginations,'orders':serializer.data})
                        return Response(data)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def ordersListDate(request):
        try:
                date_filter = datetime.datetime.now() + datetime.timedelta(days=1)
		shop_id = request.POST.get("shop_id")
                date_start = request.POST.get("date_start","2017-01-01")
		date_end1 = request.POST.get("date_end",date_filter.strftime("%Y-%m-%d"))
		date_end = datetime.datetime.strptime(date_end1, "%Y-%m-%d") + datetime.timedelta(days=1)
		if(len(shop_id)==0):
                        return JsonResponse({'detail':'The shop field can not be empty'})
                else:
			shop =Orders.objects.all().filter(shop=shop_id,date_register__range=[date_start,date_end]).extra({'date':"date(date_register)",'petition':'OK'}).values('date').annotate(count=Count('id'))	
			if(len(shop)==0):
				return JsonResponse({'petition':'EMPTY','detail':'the date fields dont have coincidence'})
			else:
				return Response(shop)
	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def ordersListDate2(request):
        try:
                date_filter = datetime.datetime.now() + datetime.timedelta(days=1)
                shop_id = request.POST.get("shop_id")
                date_start = request.POST.get("date_start","2017-01-01")
                date_end1 = request.POST.get("date_end",date_filter.strftime("%Y-%m-%d"))
                date_end = datetime.datetime.strptime(date_end1, "%Y-%m-%d") + datetime.timedelta(days=1)
                if(len(shop_id)==0):
                        return JsonResponse({'detail':'The shop field can not be empty'})
                else:
                        shop =Orders.objects.all().filter(shop=shop_id,date_register__range=[date_start,date_end]).extra({'date':"date(date_register)",'petition':'OK'}).values('date').annotate(count=Count('id'))
                        if(len(shop)==0):
                                return JsonResponse({'petition':'EMPTY','detail':'the date fields dont have coincidence'})
                        else:
                                return Response(shop)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def ordersListDateActive(request):
        try:
                date_filter = datetime.datetime.now() + datetime.timedelta(days=1)
                shop_id = request.POST.get("shop_id")
                date_start = request.POST.get("date_start","2017-01-01")
                date_end1 = request.POST.get("date_end",date_filter.strftime("%Y-%m-%d"))
                date_end = datetime.datetime.strptime(date_end1, "%Y-%m-%d") + datetime.timedelta(days=1)
                if(len(shop_id)==0):
                        return JsonResponse({'detail':'The shop field can not be empty'})
                else:
                        shop =Orders.objects.all().filter(shop=shop_id,date_register__range=[date_start,date_end],status_order_id__in=("1","2")).extra({'date':"date(date_register)",'petition':'OK'}).values('date').annotate(count=Count('id'))
                        if(len(shop)==0):
                                return JsonResponse({'petition':'EMPTY','detail':'the date fields dont have coincidence'})
                        else:
                                return Response(shop)
	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def order_detail(request, pk):
	if request.method == "GET":
		order_id = pk
		order = extended_order.objects.all().filter(order=order_id)
		if( len(order)==0):
			return JsonResponse({'detail':'The order to search does not exist','petition':'EMPTY'})
		else:
			serializer = Extended_OrderSerializers(order, many=True)
			return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def orderUsersActive(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id__in=("1","2"))
                serializer = OrderSerializerFull2(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def orderUsersSend(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id=1)[:10]
                serializer = OrderSerializerFull2(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def orderUsersConfirm(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id=2)[:10]
                serializer = OrderSerializerFull2(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def orderUsersReject(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id=3)[:10]
                serializer = OrderSerializerFull2(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def orderUsersEnd(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id=4)[:10]
                serializer = OrderSerializerFull2(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def orderUsersHistory(request, pk):
        if request.method == "GET":
                order = Orders.objects.all().filter(user_id=pk,status_order_id=4)
                serializer = OrderSerializerBasic(order, many=True)
                return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def orderUsersHistoryUsers(request,pk,page):
	try:
                shop_offsets = 5
                shop_pages = page
                if(len(pk)==0):
                        return JsonResponse({'detail':'The userPK can not be empty'})
                else:
                        shop = Orders.objects.all().filter(user_id=pk,status_order_id__in=("1","2","3","4")).order_by("-pk")
			#.order_by('shopkeeper', '-date_register')
                        if (shop_offsets==30):
                                serializer = OrderSerializerFull3(shop, many=True)
                                return Response(serializer.data)
                        else:
                                paginator = Paginator(shop, shop_offsets)
                                shop_detail = paginator.page(shop_pages)
                                serializer = OrderSerializerFull3(shop_detail, many=True)
                                Paginations = []
                                Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                                #return Response(serializer.data + Paginations)
				data = []
                       		data.append({'orders':serializer.data,'pagination':Paginations})
                        	return Response(data)

	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def pedido(request):
	try:
		order=json.loads(request.body)#request.POST['data'])

		for x in order[0]["orden"]:
			newOrders = Orders(
				user_id=order[0]["usuario"]["id"],
				user_address_id=order[0]["usuario"]["address_id"],
				shop_id=x["shop"],
				comment="Quiero la entrega lo antes posible.",#x["comment"],
				status_order_id=1,
				time="0",
				method_pay='Efectivo',
				total_quanty_products=x["cant_total_products"],
				subtotal=x["subtotal"],
				delivery_cost=x["delivery_cost"],
				total=x["total"],
				date_send=datetime.datetime.now()
			)
			newOrders.save()
			infos = info.objects.filter(pk=x["shop"])
			gcm = GCMDevice.objects.filter(user=infos[0].user)

			if( gcm[0].registration_id=='online' ):
				with SocketIO('localhost', 9090, LoggingNamespace) as socketIO:
					#notification = []
					#notification.append({"user":order[0]["usuario"]})
					#notification.append({"order":x})
					x["usuario"]=order[0]["usuario"]
					x["order_id"]=newOrders.id
					x["type"]="order"
					socketIO.emit('order',x)#notification)
					socketIO.wait(seconds=1)
			else:
				#gcm.send_message({"title":"Tiendosqui","body":{"orderID":newOrders.id,"total":newOrders.total,"message":"Ha llegado un pedido"},"status":newOrders.status_order_id })
				pass
			for j in x["products"]:
				productId = int(j["product_id"])
				pr = inventory.objects.all().filter(pk=productId)
				extended_order(
					order=newOrders,
					product_id=pr[0].id,
					quanty=j["cant"],
					price_unit=pr[0].base_price,
					subtotal=pr[0].base_price 
				).save()
		return JsonResponse({'petition':'OK','detail':'orden creada con exito!'})
	
    	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e})#'Check the fields to send, may be empty or in a wrong format'})#e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def pedidomarlon(request):
        if request.method == "POST":
                order=json.loads(request.body)
		for x in order["orden"]:
                        newOrders = Orders(
                                user_id=order["usuario"][0]["id"],
                                user_address_id=order["usuario"][0]["address_id"],
                                shop_id=x["shop"],
                                status_order_id=1,
                                time="0",
                                total_quanty_products=x["cant_total_products"],
                                subtotal=x["subtotal"],
                                delivery_cost=x["delivery_cost"],
                                total=x["total"]
                        )
                        newOrders.save()
                        infos = info.objects.filter(pk=x["shop"])
			gcm = GCMDevice.objects.filter(user=infos[0].user).send_message({"title":"Tiendosqui","body":{"orderID":newOrders.id, "total":newOrders.total,"message":"Ha llegado un pedido"},"status":newOrders.status_order_id })
			#contar = len(order["products"])
			#for j in order["products"]:
			#	return Response(contar)
				#productId = j["product_id"]
				#pr = inventory.objects
				#extended_order(
				#	order=newOrders,
				#	product_id=22#pr.id,
				#	quanty='12'#j["cant"],
				#	price_unit='3000'#pr.base_price,
				#	subtotal='3000'#pr.base_price
				#).save()
				#return Response(j)
                return JsonResponse({'petition':'OK','detail':'Order created successfully'})
	#return Response(len(order["products"]))#order["products"])#request.POST['usuarios']})
'''@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def pedidoproducts(request):
	if request.method == "POST":
		order=json.loads(request.body)
		for x in order["products"]:
		newOrders = Orders(
			user_id=order["usuario"][0]["id"],
			user_address_id=order["usuario"][0]["address_id"],
			shop_id=x["shop"],
			status_order_id=1,
			time="0",
			total_quanty_products=x["cant_total_products"],
			subtotal=x["subtotal"],
			delivery_cost=x["delivery_cost"],
			total=x["total"]
		)
		newOrders.save()
		return JsonResponse({'petition':'OK','detail':'orden creada con exito!'})'''

'''@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def pedido(request):
	if request.method == "POST":
		order=json.loads(request.body)#request.POST['data'])

		for x in order[0]["orden"]:
			newOrders = Orders(
				user_id=order[0]["usuario"][0]["id"],
				user_address_id=order[0]["usuario"][0]["address_id"],
				shop_id=x["shop"],
				status_order_id=1,
				time="0",
				total_quanty_products=x["cant_total_products"],
				subtotal=x["subtotal"],
				delivery_cost=x["delivery_cost"],
				total=x["total"]
			)
			newOrders.save()
			infos = info.objects.filter(pk=x["shop"])
			gcm = GCMDevice.objects.filter(user=infos[0].user).send_message({"title":"Tiendosqui","body":{"orderID":newOrders.id, "total":newOrders.total,"message":"Ha llegado un pedido"},"status":newOrders.status_order_id })

			for j in x["products"]:
				productId = int(j["product_id"])
				pr = inventory.objects.all().filter(product_id=productId)
				extended_order(
					order=newOrders,
					product_id=pr[0].id,
					quanty=j["cant"],
					price_unit=pr[0].base_price,
					subtotal=pr[0].base_price 
				).save()
				return Response(x["products"])'''
		#return JsonResponse({'detail':'orden creada con exito!'})
'''@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderConfirmed(request):
	if request.method == "POST":
		try:
			updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
			if updateOrder.status_order_id == 1:
				updateOrder.update(status_order_id=2,time=request.POST['time'])
				return JsonResponse({'detail':'tu orden fue confirmada con exito'})
			elif updateOrder[0].status_order_id == 2:
				return JsonResponse({'detail':'Error, tu orden ya fue confirmada anteriormente'})
			elif updateOrder[0].status_order_id == 3:
				return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
			elif updateOrder[0].status_order_id == 4:
				return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
			else:
				return JsonResponse({'detail':'La orden no existe'})
		except:
			return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe: ' })

@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderRejected(request):
	if request.method == "POST":
		try:
			updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
			if updateOrder[0].status_order_id == 1:
				newMotive = rejected_motive(
					order_id=request.POST['order_id'],
					motive=request.POST['message']
				)
				newMotive.save()
				updateOrder.update(status_order_id=3)
				return JsonResponse({'detail':'Tu orden fue rechazada con exito'})
			elif updateOrder[0].status_order_id == 2:
				updateOrder.update(status_order_id=3)
				return JsonResponse({'detail':'Tu orden fue rechazada con exito'})
			elif updateOrder[0].status_order_id == 3:
				return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
			elif updateOrder[0].status_order_id == 4:
				return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
			else:
				return JsonResponse({'detail':'La orden no existe'})
		except:
			return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe'})

@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderEnd(request):
	if request.method == "POST":
		try:
			updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
			if updateOrder[0].status_order_id == 2:
				updateOrder.update(status_order_id=4)
				#gcm = GCMDevice.objects.filter(user=updateOrder[0].user).send_message({'order':updateOrder[0].id,'message':'Tu orden fue confirmada'})
				return JsonResponse({'detail':'Tu orden fue Terminada con exito'})
			elif updateOrder[0].status_order_id == 1:
				return JsonResponse({'detail':'Error, tu orden no fue confirmada anteriormente'})
			elif updateOrder[0].status_order_id == 3:
				return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
			elif updateOrder[0].status_order_id == 4:
				return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
			else:
				return JsonResponse({'detail':'La orden no existe'})
		except:
			return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe'})

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.AllowAny,))
def ticketList(request):
	if request.method == "GET":
		shop = ticket_support.objects
		seralizer = ticketSupportSerializer(shop, many=True)
		return Response(serializer.data)


@api_view(['GET'] )
@permission_classes((permissions.AllowAny,))
def ticketListShop(request, pk):
        if request.method == "GET":
                #shop_id = request.POST.get("shop_id")
                #if(len(shop_id)==0):
                #       return JsonResponse({'detail':'The shop field can not be empty'})
                #else:
        	shop = ticket_support.objects.all().filter(order__shop_id=pk)
       		serializer = ticketSupportSerializer(shop, many=True)
        	return Response(serializer.data)- Add field date_confirm to orders
    - Add field date_end to orders
    - Add field date_reject to orders
    - Add field date_send to orders
'''

@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderConfirmed(request):
	if request.method=="POST":#try:
		#try:
		updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
		if updateOrder[0].status_order_id == 1:
			updateOrder.update(status_order_id=2,time=request.POST['time'],date_confirm=datetime.datetime.now())
			GCMDevice.objects.filter(user=updateOrder[0].user).send_message({'order':updateOrder[0].id,'message':'Tu orden fue confirmada'})
			return JsonResponse({'detail':'tu orden fue confirmada con exito'})
			
		elif updateOrder[0].status_order_id == 2:
			return JsonResponse({'detail':'Error, tu orden ya fue confirmada anteriormente'})
		elif updateOrder[0].status_order_id == 3:
			return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
		elif updateOrder[0].status_order_id == 4:
			return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
		else:
			return JsonResponse({'detail':'La orden no existe'})

		#except:
		#	return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe'})
	#except Exception as e:
        #        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderRejected(request):
	if request.method=="POST":#try:
		#updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
                #return JsonResponse(updateOrder[0].user.email,safe=False)
		#try:
		updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
			
		if updateOrder[0].status_order_id == 1:
			newMotive = rejected_motive(
				order_id=request.POST['order_id'],
				motive=request.POST['message']
			)
			newMotive.save()
			updateOrder.update(status_order_id=3, date_reject=datetime.datetime.now())
			gcm = GCMDevice.objects.filter(user=updateOrder[0].user).send_message({'order':updateOrder[0].id,'message':'Tu orden fue rechazada'})
			return JsonResponse({'detail':'Tu orden fue rechazada con exito'})
		elif updateOrder[0].status_order_id == 2:
			updateOrder.update(status_order_id=3)
			return JsonResponse({'detail':'Tu orden fue rechazada con exito'})
		elif updateOrder[0].status_order_id == 3:
			return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
		elif updateOrder[0].status_order_id == 4:
			return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
		else:
			return JsonResponse({'detail':'La orden no existe'})
		#except:
		#	return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe'})
	#except Exception as e:
        #        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'] )
@permission_classes((permissions.AllowAny,))
def orderEnd(request):
	if request.method=="POST":#try:
		#try:
		updateOrder = Orders.objects.all().filter(pk=request.POST['order_id'])
		if updateOrder[0].status_order_id == 2:
			updateOrder.update(status_order_id=4, date_end=datetime.datetime.now())
			gcm = GCMDevice.objects.filter(user=updateOrder[0].user).send_message({'order':updateOrder[0].id,'message':'Tu orden finalizo'})
			return JsonResponse({'detail':'Tu orden fue Terminada con exito'})
		elif updateOrder[0].status_order_id == 1:
			return JsonResponse({'detail':'Error, tu orden no fue confirmada anteriormente'})
		elif updateOrder[0].status_order_id == 3:
			return JsonResponse({'detail':'Error, tu orden ya fue rechazada anteriormente'})
		elif updateOrder[0].status_order_id == 4:
			return JsonResponse({'detail':'Error, tu orden ya fue culminada'})
		else:
			return JsonResponse({'detail':'La orden no existe'})
		#except:
		#	return JsonResponse({'detail':'La orden: '+str(request.POST['order_id'])+' No existe'})
	#except Exception as e:
                #return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def ultimateFiveOrdersShop(request,pk):
        if request.method == "GET":
                orders = Orders.objects.all().filter(shop_id=pk).order_by('-pk')[:5]
                serializer = OrderSerializerFull3(orders, many=True)
		data1 = json.dumps(serializer.data)
                data2 = json.loads(data1)

                for x in data2:
                        phone = Profile.objects.all().filter(user_id=x['user']['id'])
                        if len(phone)==0:
				x['user'].update({"phone":"null"})
			else:
				x['user'].update({"phone":phone[0].phone})
                return Response(data2)	

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchOrderId(request):
        try:
                data = json.loads(request.body)
                if(len(data["search_id"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                order = Orders.objects.all().filter(pk=data["search_id"])
                serializer = OrderSerializerFull3(order, many=True)#OrderSerializerBasic(order, many=True)
    		data1 = json.dumps(serializer.data)
                data2 = json.loads(data1)

                for x in data2:
               		phone = Profile.objects.all().filter(user_id=x['user']['id'])
                        if len(phone)==0:
                                x['user'].update({"phone":"null"})
                        else:
                                x['user'].update({"phone":phone[0].phone})
            
		if (len(order)>0):
                        return Response(data2)
                else:
                        return Response({'petition':'OK','detail':'The order you are looking for do not exist'})
        except product.DoesNotExist:
                return JsonResponse({"petition":"DENY","detail":"The order does not exist"})

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def statusList(request):
        try:
                orders = status.objects.all().filter()[:4]
                serializer = StatusSerializersBasic(orders, many=True)
                return Response(serializer.data)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addTicketUsers(request):
        try:
		motives = request.POST['motive'] 
		orderID = request.POST['order_id']
		ticketList=ticket_support.objects.all().filter(order_id=orderID)
		if(len(ticketList)>0):
			return Response({'detail':'A ticket already exists for your order, and has the status: '+ticketList[0].status.name,'petition':'OK'})
		else:
              		ticket = ticket_support(type_user_id =1,order_id=orderID ,motive=motives,status_id=1)
                	ticket.save()
                	return Response({'detail':'Ticket created successfully','petition':'OK'})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
'''
pedidos generados   [x]
compras totales     [x]
horario mas activo  []
tienda mas pedida   [x]
'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def summaryHistoryBuyer(request,pk):
        if request.method == "GET":
                	
                shopWithMorePurchases =Orders.objects.filter(user_id=pk).values('shop_id').annotate(dcount=Count('shop_id'))
                shopNumberOne = max(shopWithMorePurchases)
		shop = info.objects.filter(pk=shopNumberOne["shop_id"])
		shopNumberOne["shop_name"]=shop[0].name
		sales =Orders.objects.filter(user_id=pk).aggregate(Sum('total')).get('total__sum')
                pedidos = Orders.objects.filter(user_id=pk).aggregate(Count('id')).get('id__count')
                #newUsers = User.objects.all().filter(date_joined__contains=date).aggregate(Count('id')).get('id__count')
                summaryDaily = []
                summaryDaily.append({'shops_open':shopNumberOne,'total_sales':sales, 'total_orders':pedidos,"most_active_hour":{"from":"14:00","to":"15:00"} })
                return JsonResponse(summaryDaily,safe=False)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def changeTicketUsers(request):
        try:
                order_id = request.POST.get("order_id")
                ticket_status = request.POST.get("ticket_status")
	
		if order_id is None:
			return JsonResponse({'petition':'EMPTY','detail':'The ticket_id field can not be empty'})

		if ticket_status is None:
			return JsonResponse({'petition':'EMPTY','detail':'The ticket_status field can not be empty'})
		
		if ticket_status == "1":
			return JsonResponse({'petition':'ERROR','detail':'You can not assign a ticket to a ticket'})

		ticket = ticket_support.objects.all().filter(order_id=order_id)
		
		if len(ticket)==0:
			return JsonResponse({'petition':'EMPTY','detail':'The ticket does not exist'})
		else:
			#valida que no puede cerrar un ticket sin procesar
			if( (ticket[0].status_id == 1) and (ticket_status=="2") ):
				#ticket[0].update(status_id=int(ticket_status))
				#return JsonResponse({'petition':'OK','detail':'The ticket_status change to: '+ticket[0].status.name})
				return JsonResponse({'petition':'OK','detail':'You can not close a ticket if you have not processed it'})
			#si acciones cerraro y ticket esta cerrado
			elif( (ticket[0].status_id == 2) and (ticket_status=="2") ):
				return JsonResponse({'petition':'DUPLY','detail':'The ticket is already finished'})
			#si esta cerrado y lo quieres volver a procesar
			elif( (ticket[0].status_id == 2) and (ticket_status=="3") ):
				ticket.update(status_id=int(ticket_status))
                                return JsonResponse({'petition':'OK','detail':'The ticket_status change to: '+ticket[0].status.name})
			#si esta ya en proceso y el estatus manda a procesar de nuevo
			elif( (ticket[0].status_id == 3) and (ticket_status=="3") ):
                                return JsonResponse({'petition':'DUPLY','detail':'The ticket is already in process'}) 
			#en proceso
			elif( (ticket[0].status_id == 1) and (ticket_status=="3") ):
                                ticket.update(status_id=int(ticket_status))
				#return Response(ticket[0].id)
                                return JsonResponse({'petition':'OK','detail':'The ticket_status change to: '+ticket[0].status.name})
			#cerrar un ticket
                        elif( (ticket[0].status_id == 3) and (ticket_status=="2") ):
                                ticket.update(status_id=int(ticket_status))
                                #return Response(ticket[0].id)
                                return JsonResponse({'petition':'OK','detail':'The ticket_status change to: '+ticket[0].status.name})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
