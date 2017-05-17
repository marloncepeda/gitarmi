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
		user =  Orders.objects.all().filter(pk=data["order_id"])
		rateUsers = qualifications_shop(
			user_id = user[0].user_id,
			shop_id = user[0].shop_id,
			order_id = data["order_id"],
			rate = data["rate"],
			comment = data["comment"]
		)
		rateUsers.save() 
		return JsonResponse({'detail':'The buyer was successfully qualified','petition':'OK'})
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyShopHistory(request):
	try:
		shopId = request.POST["shop_id"]
		history = qualifications_shop.objects.all().filter(shop_id=shopId)
		serializers = qualificationsShopSerializer(history, many=True)
		return JsonResponse(serializers.data)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyUserHistory(request):
	try:
		userId = request.POST["user_id"]
		history = qualifications_user.objects.all().filter(user_id=userId)
		serializers = qualificationsUserSerializer(history, many=True)
		return JsonResponse(serializers.data)
	except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

