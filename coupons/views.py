from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from .models import *
from .serializers import *
from django.http import Http404
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def createStartCoupon(request):
	if request.method == "POST":
		data=json.loads(request.POST['data'])
		return JsonResponse(data)
		'''
		shop_id = request.POST.get("coupon_name")
		if(len(shop_id)==0): 
			return JsonResponse({'petition':'EMPTY','detail':'The shop field can not be empty'})
		else:
			shop = Orders.objects.all().filter(shop=shop_id)
			serializer = OrderSerializerBasic(shop, many=True)
			return Response(serializer.data)
		'''