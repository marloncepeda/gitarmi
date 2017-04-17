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
	if request.method == "POST":
		data = json.loads(request.POST["data"])
		order =  Orders.objects.all().filter(pk=data[0]["order_id"])
		rateq =  qualifications_user.objects.all().filter(order_id=order[0].id)

		if(len(rateq)>0): 
			return JsonResponse({'detail':'La orden: '+ str(data[0]["order_id"]) +' ya tiene calificacion','serverResponse':'Deny'})
		elif order[0].status_order_id == 1 or order[0].status_order_id == 2 or order[0].status_order_id == 3 : 
			return JsonResponse({'detail':'La orden: '+ str(data[0]["order_id"]) +' aun no esta finalizada.','serverResponse':'Deny'})
		else:
			rateUsers = qualifications_user(
				user_id = order[0].user_id,
				shop_id = order[0].shop_id,
				order_id = data[0]["order_id"],
				rate = data[0]["rate"],
				comment = data[0]["comment"]
			)
			rateUsers.save() 
			return JsonResponse({'detail':'The buyer was successfully qualified','serverResponse':'ok'})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyShop(request):
	if request.method == "POST":
		data = json.loads(request.POST["data"])
		user =  Orders.objects.all().filter(pk=data[0]["order_id"])
		rateUsers = qualifications_shop(
			user_id = user[0].user_id,
			shop_id = user[0].shop_id,
			order_id = data[0]["order_id"],
			rate = data[0]["rate"],
			comment = data[0]["comment"]
		)
		rateUsers.save() 
		return JsonResponse({'detail':'The buyer was successfully qualified'})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyShopHistory(request):
	if request.method == "POST":
		shopId = request.POST["shop_id"]
		history = qualifications_shop.objects.all().filter(shop_id=shopId)
		serializers = qualificationsShopSerializer(history, many=True)
		return JsonResponse(serializers.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def QualifyUserHistory(request):
	if request.method == "POST":
		userId = request.POST["user_id"]
		history = qualifications_user.objects.all().filter(user_id=userId)
		serializers = qualificationsUserSerializer(history, many=True)
		return JsonResponse(serializers.data)