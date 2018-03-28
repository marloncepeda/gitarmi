from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render
from .models import *
from .serializers import *
from django.core.paginator import Paginator
from django.db.models import Sum,Max,Count,Avg
import json

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def registerUserss(request):
        if request.method == "POST":
                user = json.loads(request.body)
                if len(user["email"])==0:
                        return JsonResponse({'petition':'EMTPY','detail':'Fields can not be empty'})

                try:
                        new_user = User.objects.create_user(user["email"],user["email"],user["password"])
                        new_user.is_active = True
                        new_user.first_name = user["name"]
                        new_user.save()
                        profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=1, status_id=1)
                        profile_user.save()

                except Exception as e:
                        return JsonResponse({'petition':'DENY','detail':'user already exists' })


def changePassword(request):
        if request.method == 'POST':
                u = User.objects.get(username__exact=str(request.POST.get("email")) )
                u.set_password(request.POST.get("password1") )
                u.save()
                return HttpResponse('Clave de usuario cambiada ')


