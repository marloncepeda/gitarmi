from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from orders.models import Orders
from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Sum,Max,Count,Avg
import json

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyUser(request):
	try:
		data = json.loads(request.body)
		order =  Orders.objects.all().filter(pk=data["order_id"])
		rateq =  qualifications_user.objects.all().filter(order_id=order[0].id)

		if(len(rateq)>0): 
			return JsonResponse({'detail':'La orden: '+ str(data["order_id"]) +' ya tiene calificacion','petition':'Deny'})
		elif order[0].status_order_id == 1 or order[0].status_order_id == 2 or order[0].status_order_id == 3 : 
			return JsonResponse({'detail':'La orden: '+ str(data["order_id"]) +' aun no esta finalizada.','petition':'Deny'})
		else:
			rateUsers = qualifications_user(
				user_id = order[0].user_id,
				shop_id = order[0].shop_id,
				order_id = data["order_id"],
				rate = data["rate"],
				comment = data["comment"]
			)
			rateUsers.save() 
			return JsonResponse({'detail':'The buyer was successfully qualified','petition':'ok'})
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyShop(request):
	try:
		data = json.loads(request.body)
		if data["order_id"] is None:
			return JsonResponse({'petition':'EMPTY','detail':'the field order_id does not null'})

		user =  Orders.objects.all().filter(pk=data["order_id"])
		if len(user)==0:
			return JsonResponse({'petition':'EMPTY','detail':'You can not qualify an order that does not exist'})
		else:
			'''rateUsers = qualifications_shop(
				user_id = user[0].user_id,
				shop_id = user[0].shop_id,
				order_id = data["order_id"],
				rate = data["rate"],
				comment = data["comment"]
			)
			rateUsers.save()'''
			qualify =qualifications_shop.objects.all().filter(shop_id= user[0].shop_id).aggregate(Sum('rate'),Count('id'))#.get('rate__sum')
			q = qualify["rate__sum"]/qualify["id__count"]
			return JsonResponse(round(q, 1),safe=False)
			TotalQualify = len(qualify)
		return JsonResponse({'detail':'The buyer was successfully qualified','petition':'OK'})
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyShopHistory(request):
	try:
                shop_id = request.POST.get("shop_id")
                shop_offsets = request.POST.get("offset",10)
                shop_pages = request.POST.get("page",1)

                if shop_id is None:
                        return JsonResponse({'detail':'The shop_id field can not be empty'})
                else:
			shop = qualifications_shop.objects.all().filter(shop_id=shop_id)
			paginator = Paginator(shop, shop_offsets)
                       	shop_detail = paginator.page(shop_pages)
                        serializer = qualificationsShopSerializer(shop_detail, many=True)
                        Paginations = []
                        Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
			data = []
			data.append({'qualify':serializer.data,'paginations':Paginations})
                        return Response(data)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyUserHistory(request):
	try:
                user_id = request.POST.get("user_id")
                shop_offsets = request.POST.get("offset",10)
                shop_pages = request.POST.get("page",1)

                if user_id is None:
                        return JsonResponse({'detail':'The user_id field can not be empty'})
                else:
                        shop = qualifications_user.objects.all().filter(user_id=user_id)
                        paginator = Paginator(shop, shop_offsets)
                        shop_detail = paginator.page(shop_pages)
                        serializer = qualificationsUserSerializer(shop_detail, many=True)
                        Paginations = []
                        Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                        data = []
                        data.append({'qualify':serializer.data,'paginations':Paginations})
                        return Response(data)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
