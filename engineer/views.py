from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
#from orders.models import Orders
from .models import *
from users.models import Profile
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Sum,Max,Count,Avg
import json

#api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
#def createStartCoupon(request):
#	if request.method == "POST":
#		data=json.loads(request.POST['data'])
#		return JsonResponse(data)
#		'''
#		shop_id = request.POST.get("coupon_name")
#		if(len(shop_id)==0): 
#			return JsonResponse({'petition':'EMPTY','detail':'The shop field can not be empty'})
#		else:
#			shop = Orders.objects.all().filter(shop=shop_id)
#			serializer = OrderSerializerBasic(shop, many=True)
#			return Response(serializer.data)
#		'''

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def changeAvailability(request):
        try:
                data = json.loads(request.body)
		#validStatus = statusEngineer.objects.all().filter(status_id =data["status_id"], engineer_id=data["engineer_id"]).order_by('-date_register')[:1]
		#if len(validStatus)==0:
               	statusNew = statusEngineer(
                       	engineer_id= data["engineer_id"],
                       	status_id = data["status_id"]
                )
                statusNew.save()
                return JsonResponse({'detail':'the engineer availability has been changed','petition':'ok'})
        except Exception as e:
		return JsonResponse({'detail':e.message,'petition':'ERROR'})
