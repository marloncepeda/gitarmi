from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import *
from users.models import Profile
from .serializers import *
import json

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
