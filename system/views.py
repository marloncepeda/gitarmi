from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from django.http import JsonResponse, Http404,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import *
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.contrib.auth import get_user_model
from .models import *
from .serializers import *
from django.contrib.auth.forms import PasswordChangeForm
import json
import sendgrid
import os
from sendgrid.helpers.mail import *
from push_notifications.gcm import gcm_send_message
from push_notifications.models import GCMDevice

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def terms(request):
        if request.method == 'GET':
                terms = termsAndConditions.objects.all().order_by('-pk')[:1]
                serializer = TermsSerializer(terms, many=True)
                return Response(serializer.data)

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getPhones(request):
        if request.method == 'GET':
                companyPhones = company.objects.all().order_by('-pk')
                serializer = CompanyPhonesSerializer(companyPhones, many=True)
                return Response(serializer.data)

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def requestCallUser(request):
        if request.method == 'POST':
                companyPhones = company.objects.all().order_by('-pk')
                serializer = CompanyPhonesSerializer(companyPhones, many=True)
                return Response(serializer.data)
