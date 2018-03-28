from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from .models import *
from .serializers import *
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
