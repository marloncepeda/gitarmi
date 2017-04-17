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
import re
from sendgrid.helpers.mail import *
from push_notifications.gcm import gcm_send_message
from push_notifications.models import GCMDevice

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def deviceusers(request):
	try:
		data = json.loads(request.body)
		try:
			gcm =GCMDevice.objects.get(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
			gcm.save()
			return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
		except GCMDevice.DoesNotExist:
			gcm = GCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
			gcm.save()
			return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})
	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'})#e.message})

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def getProfile(request, pk):
        if request.method == 'GET':
               ProfileSerializer

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def postProfile(request):
        if request.method == 'POST':
               pass
'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def preRegisterUsers(request):
	if request.method == "POST":
		user = json.loads(request.body)
		
		if len(user["email"])==0:
			return JsonResponse({'petition':'EMTPY','detail':'Fields can not be empty'})

		match=re.search(r'(\d+-\d+-\d+)',user["birthdate"])
		if match is None:
			return JsonResponse({'petition':'BAD FORMAT','detail':'The birthday field does not have the desired format: DD-MM-AAAA'})
		try:	
			new_user = User.objects.create_user(user["email"],user["email"],user["password"])
			new_user.is_active = False
			new_user.first_name = user["name"]
			new_user.save()
			profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=1, birthdate=user["birthdate"],status_id=1)
 			profile_user.save()
		
			sg = sendgrid.SendGridAPIClient(apikey=settings.SENGRID_KEY)
			from_email = Email("marloncepeda@tiendosqui.com")
			subject = "Activar usuario Tiendosqui"
			to_email = Email(user["email"])
			content = Content("text/html", "Activar usuario Tiendosqui")
			mail = Mail(from_email, subject, to_email, content)
			mail.personalizations[0].add_substitution(Substitution("NOMBREUSUARIO", user["name"]))
			mail.personalizations[0].add_substitution(Substitution("LINKACTIVADOR", 'devtiendosqui.cloudapp.net/v2/users/activate/?emailact='+user["email"]))
			mail.set_template_id("7b27602d-92dd-4ab3-9d90-9d9b1c7c2ef7")
			try:
				response = sg.client.mail.send.post(request_body=mail.get())
				return JsonResponse({'petition':'OK','detail':'Enviado correo para verificar usuario'})
			except urllib.HTTPError as e:
				return JsonResponse({'petition':'OK','detail':'Enviado correo para verificar usuario'})
		except Exception as e:
			return JsonResponse({'petition':'DENY','detail':'user already exists' })

def activateUsers(request):
        if request.method == "GET":
		email_user = request.GET.get('emailact')
		user = User.objects.get(email=email_user)
		user.is_active = True
		user.save()
		context = {'question': request.GET.get('emailact')}
                return render(request, '/webapps/hello_django/backend-nuevo/users/templates/activateusers.html', context)
		#return Response('Tu cuenta fue activada con exito :)')

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def addressAdd(request):
	try:
                data = json.loads(request.body)
                ids = data["usersids"]
		name= data["addressname"]
		dir = data["addressformated"]
		detail = data["addressdetail"]
		lati = data["addresslat"]
		lngt = data["addresslon"]
		AdresConfirm = Address.objects.all().filter(client_id=ids, address_alias=name, address=dir, address_detail=detail, lat=lati, lon=lngt)
		if(len(AdresConfirm)==0):
		
			addressModel = Address(client_id=ids, address_alias=name, address=dir, address_detail=detail, lat=lati, lon=lngt)
			addressModel.save()
                	return JsonResponse({'petition':'OK','idaddress':addressModel.id})
		else:
			return JsonResponse({'petition':'DENY','detail':'The user has an equal address'})
	
	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'})#e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def sendEmailPassword(request):
	if request.method == "POST":
		data = json.loads(request.body)
		emailu = data["user_email"]
		try:	
			profile = User.objects.all().filter(email=emailu)
			sg = sendgrid.SendGridAPIClient(apikey=settings.SENGRID_KEY)
			from_email = Email("info@tiendosqui.com")
			subject = "Activar usuario Tiendosqui"
			to_email = Email(profile[0].email)
			content = Content("text/html", "Activar usuario Tiendosqui")
			mail = Mail(from_email, subject, to_email, content)
			mail.personalizations[0].add_substitution(Substitution("[USUARIOCORREO]", emailu))
			mail.personalizations[0].add_substitution(Substitution("[LINKACTIVADOR]", "devtiendosqui.cloudapp.net/v2/users/change/password/?id="+profile[0].email))
			mail.set_template_id("fdb80714-594d-4f74-86d8-aae37f36166b")
			try:
				response = sg.client.mail.send.post(request_body=mail.get())
				return JsonResponse({'petition':'OK','detail':'Sent email to change password'})
			except urllib.HTTPError as e:
				return JsonResponse({'petition':'ERROR','detail':'Error sernding email'})
		except:
			return JsonResponse({'petition':'DENY','detail':'Email error: '+data["user_email"]+' does not exist'})

def changeEmailPassword(request):
	if request.method == "GET":
		#user = User.objects.all().filter(email="warlhunters@gmail.com")
		context = {'question': request.GET.get('id')}
		return render(request, '/webapps/hello_django/backend-nuevo/users/templates/changepassword.html', context)
	elif request.method == "POST":
		#http://devtiendosqui.cloudapp.net/v2/users/change/password/?id=marloncepeda@gmail.com
		return Response(request.body)
'''
def changeEmailPassword(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('accounts:change_password')
		else:
			messages.error(request, 'Please correct the error below.')
	else:
		form = PasswordChangeForm(request.user)
		return render(request, '/webapps/hello_django/backend-nuevo/users/templates/changepassword.html', {'form': form})
'''
@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def profile(request, pk):
	if request.method == 'GET':
		profile = Profile.objects.all().filter(user=pk)
		serializer = ProfileSerializer(profile, many=True)
		return Response(serializer.data)

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
def profileUpdate(request):
        try:
        	userid = request.POST.get('user_id')
		phone = request.POST.get('user_phone')
		email = request.POST.get('user_email')
		name = request.POST.get('user_name')
		#image = request.FILES["user_image"]
		if( (len(userid)==0)or(len(phone)==0)or(len(email)==0)or(len(name)==0) ):
			return JsonResponse({'petition':'EMPTY','detail':'The fields not null'})
		else:
       			user = User.objects.get(pk=userid)
			profile = Profile.objects.filter(user_id=userid)
        		user.last_name = name
			user.email = email
			user.username = email
        		user.save()
			profile.update(phone=phone)#pictures =image, phone = phone)
        		return JsonResponse({'petition':'OK','detail':'The user was successfully changed'})
	except User.DoesNotExist:
        	return JsonResponse({"petition":"DENY","detail":"User does not exist"})
	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET', 'POST','PUT'])
@permission_classes((permissions.AllowAny,))
def confirmAccount(request):
    if request.method == 'GET':
        profile = Profile.objects.all().filter(user=request.POST.get("user_id"))
        serializer = ProfileSerializer(profile, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        try:
            username = User.objects.all().filter(email=request.POST.get("shop_id"))        
            return JsonResponse({'Petition':'OK','menssage':'si existe'})

        except:
            return JsonResponse({'Petition':'DENY','menssage':'No existe el usuario'})

@api_view(['DELETE'])
@permission_classes((permissions.AllowAny,))
#@staff_member_required 
def del_user(request):#, username):    
    try:
        u = User.objects.get(pk = request.POST["id_user"])
        u.delete()
        return JsonResponse({"petition":"OK","detail":"The user is deleted"})            

    except User.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})    

    except Exception as e: 
        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['PUT'])
@permission_classes((permissions.AllowAny,))
#@staff_member_required 
def suspendActivateUser(request):#, username):    
    try:
        u = User.objects.get(pk = request.POST["id_user"])
        if(request.POST["status"]=="Suspender"):
		u.is_active = False
		u.save()
       		return JsonResponse({"petition":"OK","detail":"The user is suspended"})
	elif(request.POST["status"]=="Activar"):
		u.is_active = True
                u.save()
                return JsonResponse({"petition":"OK","detail":"The user is activated"})
	else:
		return JsonResponse({"petition":"EMTPY","detail":"The fields status is not null"})
    except User.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})

    except Exception as e:
        return JsonResponse({"petition":"ERROR","detail":e.message})



