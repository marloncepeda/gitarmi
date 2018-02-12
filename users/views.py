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
from django.core.paginator import Paginator
from orders.models import extended_order
from django.db.models import F,Count
from orders.models import Orders
from orders.serializers import ordersBasicSerializerUser
#from fcm_django.models import FCMDevice

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def deviceusers(request):
#	return HttpResponse("servicio en test jenkinks")
	try:
		data = json.loads(request.body)
		fcm = GCMDevice.objects.all().filter(user_id=data["userid"])
#		return HttpResponse(fcm[0].user)
		if len(fcm)==0:
			fcm1 = GCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name="usuario",type=data["type_device"])
			fcm1.save()
                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
                else:
                        fcm[0].registration_id=data["users_deviceid"]
                        fcm[0].save()
                        return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})
                '''try:
                        gcm =GCMDevice.objects.get(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
                        gcm.save()
                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
                except GCMDevice.DoesNotExist:
                        gcm = GCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
                        gcm.save()
                        return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})'''
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'}) #e.message})

#@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
#def deviceusers(request):
#        try:
#                data = json.loads(request.body)
#                fcm = FCMDevice.objects.all().filter(user=data["userid"])
#                #return HttpResponse(fcm[0].user)
#                if len(fcm)==0:
#                        fcm1 = FCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name="usuario",type=data["type_device"])
#                        fcm1.save()
#                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
#                else:
#                        fcm[0].registration_id=data["users_deviceid"]
#                        fcm[0].save()
#                        return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})
#                '''try:
#                        gcm =GCMDevice.objects.get(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
#                        gcm.save()
#                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
#                except GCMDevice.DoesNotExist:
#                        gcm = GCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
#                        gcm.save()
#                        return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})'''
#        except Exception as e:
#                return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'}) #e.message})

#@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
#def deviceusers(request):
#	try:
#		data = json.loads(request.body)
		#fcm = FCMDevice.objects.all().filter(user=data["userid"])
                #if len(fcm)==0:
                #        fcm1 = FCMDevice(registration_id=data["users_deviceid"],user=data["userid"],name=profile[0].name)
                #        fcm1.save()
		#	return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
                #
#		fcm = FCMDevice.objects.all().filter(user=data["userid"])
                #return HttpResponse(fcm[0].user)
#                if len(fcm)==0:
#                        fcm1 = FCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name="usuario",type=data["type_device"])
#                        fcm1.save()
#                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
#		else:
#                        fcm[0].registration_id=data["users_deviceid"]
#                        fcm[0].save()
#			return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})
		'''try:
			gcm =GCMDevice.objects.get(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
			gcm.save()
			return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
		except GCMDevice.DoesNotExist:
			gcm = GCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name='usuario')
			gcm.save()
			return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})'''
#	except Exception as e:
#		return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'})#e.message})

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

		if 'stratum' not in user:
			return JsonResponse({'petition':"EMPTY","detail":"Field stratum can not be empty"})
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
			from_email = Email("Willy@tiendosqui.com")
			subject = "Activar usuario Pediidos"
			to_email = Email(user["email"])
			content = Content("text/html", "Activar usuario Pediidos")
			mail = Mail(from_email, subject, to_email, content)
			mail.personalizations[0].add_substitution(Substitution("NOMBREUSUARIO", user["name"]))
			mail.personalizations[0].add_substitution(Substitution("LINKACTIVADOR", 'apitest.pediidos.com/v2/users/activate/?emailact='+user["email"]))
			mail.set_template_id("7b27602d-92dd-4ab3-9d90-9d9b1c7c2ef7")
			try:
				response = sg.client.mail.send.post(request_body=mail.get())
				return JsonResponse({'petition':'OK','detail':'Enviado correo para verificar usuario',"userid":new_user.id})
			except urllib.HTTPError as e:
				return JsonResponse({'petition':'OK','detail':'Enviado correo para verificar usuario'})
		except Exception as e:
			return JsonResponse({'petition':'DENY','detail':'user already exists' })

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def AdminAddUsers(request):
	if request.method == "POST":
		user = json.loads(request.body)		
		
		'''if len(user["user_id"])==0:
			return JsonResponse({'petition':'EMTPY','detail':'Fields can not be empty'})
		else:
			user = User.objects.get(pk=user["user_id"])
                	user.is_active = True	
			return HttpResponse('se logro')'''
		match=re.search(r'(\d+-\d+-\d+)',user["birthdate"])
		if match is None:
			return JsonResponse({'petition':'BAD FORMAT','detail':'The birthday field does not have the desired format: DD-MM-AAAA'})
		try:	
			new_user = User.objects.create_user(user["email"],user["email"],user["password"],)
			new_user.is_active = False
			#new_user.save()
			new_user.is_staff=user["supervendedor"]
			new_user.is_superuser = user["admin"]
			new_user.first_name = user["name"]
			new_user.save()
			profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=1, birthdate=user["birthdate"],status_id=1)
 			profile_user.save()
			
			sg = sendgrid.SendGridAPIClient(apikey=settings.SENGRID_KEY)
			from_email = Email("Willy@tiendosqui.com")
			subject = "Activar usuario Pediidos"
			to_email = Email(user["email"])
			content = Content("text/html", "Activar usuario Pediidos")
			mail = Mail(from_email, subject, to_email, content)
			mail.personalizations[0].add_substitution(Substitution("NOMBREUSUARIO", user["name"]))
			mail.personalizations[0].add_substitution(Substitution("LINKACTIVADOR", 'apitest.pediidos.com/v2/users/activate/?emailact='+user["email"]))
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
                return render(request, '/webapps/hello_django/server-tiendosqui/users/templates/activateusers.html', context)
		#return Response('Tu cuenta fue activada con exito :)')

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def addressAdd(request):
	try:
                data = json.loads(request.body)
                ids = str(data["usersids"])
		name= data["addressname"]
		dir = data["addressformated"]
		detail = data["addressdetail"]
		lati = data["addresslat"]
		lngt = data["addresslon"]
		uniqueid = data["uniqueid"]

		if 'city' not in data:
                        cityAddress = "null"
                else:
                        cityAddress = data["city"]

		if( (len(ids)==0) or (len(name)==0) or (len(dir)==0) or (len(lati)==0) or (len(lngt)==0) ):
			return JsonResponse({'detail':'Fields can not be null','petition':'EMPTY'})

		AdresConfirm = Address.objects.all().filter(client_id=ids, address_alias=name, address=dir, address_detail=detail, lat=lati, lon=lngt)
		if(len(AdresConfirm)==0):
			addressModel = Address(client_id=ids, city=cityAddress, unique_id=uniqueid, address_alias=name, address=dir, address_detail=detail, lat=lati, lon=lngt)
			addressModel.save()
                	return JsonResponse({'petition':'OK','idaddress':addressModel.id})
		else:
			return JsonResponse({'petition':'DENY','detail':'The user has an equal address'})

	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":'Check the fields to send, may be empty or in a wrong format'})#e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def getAddress(request):
        try:
                data = json.loads(request.body)
                ids = data["user_id"]
		cant = data["user_cant"]
		if cant==0:
			address = Address.objects.all().filter(client_id=ids)
		else:
			address = Address.objects.all().filter(client_id=ids)[:cant]

		serializer = AddressSerializerFull(address, many=True)
                if(len(address)==0):
			return JsonResponse({'petition':'OK','detail':'The user has no saved addresses'})
                else:
                        return Response(serializer.data)

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
			from_email = Email("Willy@tiendosqui.com")
			subject = "Activar usuario Pediidos"
			to_email = Email(profile[0].email)
			content = Content("text/html", "Activar usuario Pediidos")
			mail = Mail(from_email, subject, to_email, content)
			mail.personalizations[0].add_substitution(Substitution("[USUARIOCORREO]", emailu))
			mail.personalizations[0].add_substitution(Substitution("[LINKACTIVADOR]", "apitest.pediidos.com/v2/users/change/password/?id="+profile[0].email))
			mail.set_template_id("fdb80714-594d-4f74-86d8-aae37f36166b")
			try:
				response = sg.client.mail.send.post(request_body=mail.get())
				return JsonResponse({'petition':'OK','detail':'Sent email to change password'})
			except urllib.HTTPError as e:
				return JsonResponse({'petition':'ERROR','detail':'Error sernding email'})
		except:
			return JsonResponse({'petition':'DENY','detail':'Email error: '+data["user_email"]+' does not exist'})
'''
def changeEmailPassword(request):
	if request.method == "GET":
		#user = User.objects.all().filter(email="warlhunters@gmail.com")
		context = {'question': request.GET.get('id')}
		return render(request, '/webapps/hello_django/server-tiendosqui/users/templates/changepassword.html', context)
	elif request.method == "POST":
		#http://devtiendosqui.cloudapp.net/v2/users/change/password/?id=marloncepeda@gmail.com
		return Response(request.body)
'''
def changeEmailPassword(request):
	if request.method == 'POST':
		userData = User.objects.get(email=request.POST["email"])
		#if len(userData)==0:
		#	return HttpResponse('El usuario no existe')
		#else:
		#	form = PasswordChangeForm(request.user, request.POST)
		return HttpResponse('Clave de usuario cambiada')
		'''if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			return redirect('accounts:change_password')
		else:
			messages.error(request, 'Please correct the error below.')'''
	else:
		#form = PasswordChangeForm(request.user)
		return render(request, '/webapps/hello_django/server-tiendosqui/users/templates/changepassword.html', {'question': request.GET.get('id')}) #{'form': form})

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
		phone = request.POST.get('user_phone',"null")
		email = request.POST.get('user_email',"null")
		name = request.POST.get('user_name',"null")
		if 'user_image' not in request.FILES:
			image = "null"
		else:
			image = request.FILES['user_image']	

       		user = User.objects.get(pk=userid)
		profile = Profile.objects.filter(user_id=userid)
			
		if name is not "null":
        		user.first_name = name
			user.save()
		if phone is not "null":
			profile.update(phone=phone)
		if email is not "null":
			user.email = email
			user.username = email
        		user.save()
		if image is not "null":
			imagePath = imagePath = '/webapps/hello_django/server-tiendosqui/misitio/'+image.name
            		destination = open(imagePath, 'wb+')
            		for chunk in image.chunks():
                    		destination.write(chunk)
            		destination.close()

            		profile.update(pictures = image)

        	return JsonResponse({'petition':'OK','detail':'The user was successfully changed'})
	except User.DoesNotExist:
        	return JsonResponse({"petition":"DENY","detail":"User does not exist"})
	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e.message })

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
	profile = Profile.objects.all().filter(user_id=request.POST["id_user"])
        if(request.POST["status"]=="Suspender"):
		u.is_active = False
		u.save()
		profile.update(status_id=3)
       		return JsonResponse({"petition":"OK","detail":"The user is suspended"})
	elif(request.POST["status"]=="Activar"):
		u.is_active = True
                u.save()
		profile.update(status_id=1)
                return JsonResponse({"petition":"OK","detail":"The user is activated"})
	else:
		return JsonResponse({"petition":"EMTPY","detail":"The fields status is not null"})
    except User.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})

    except Exception as e:
        return JsonResponse({"petition":"ERROR","detail":e.message})

'''
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def allUsers(request):    
    try:
        u = Profile.objects
        serializer = ProfileSerializer(u,many=True)
	return Response(serializer.data)
    except User.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})

    except Exception as e:
        return JsonResponse({"petition":"ERROR","detail":e.message})
'''
@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def allUsers(request):
        try:
                shop_offsets = request.POST.get("offset",30)
                shop_pages = request.POST.get("page",1)
		status = request.POST.get("status_profile",3)
                shop = Profile.objects.all().filter(type_user__name="Comprador",status_id=status)
		if (len(shop)==0):
			return JsonResponse({'petiton':'EMPTY','detail':'does not exist buyer user with status: '+status})
		else:
                	paginator = Paginator(shop, shop_offsets)
                	shop_detail = paginator.page(shop_pages)
                	serializer = ProfileSerializer(shop_detail, many=True)
                	Paginations = []
                	Paginations.append({'num_pages':paginator.num_pages,'actual_page':shop_pages})
                	data = []
			for user in serializer.data:
				order = Orders.objects.all().filter(user_id=user["user"]["id"]).order_by("-pk")[:1]
				serializer2 = ordersBasicSerializerUser(order,many=True)

				Totalorder = Orders.objects.all().filter(user_id=user["user"]["id"], status_order=1).values('user').annotate(dcount=Count('user'))
				if (len(Totalorder)==0):
					user["order"]= {'total_order_end':0,'last_order':serializer2.data }
				else:
					user["order"]= {'total_order_end':Totalorder,'last_order':serializer2.data }
	        	#return JsonResponse(serializer.data,safe=False)
                	data.append({'users':serializer.data,'pagination':Paginations})
                	return Response(data)
	except Exception as e:
 	       return JsonResponse({"petition":"ERROR","detail":e})

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def allAddressUsers(request,pk):
        try:
                address_offsets = request.GET.get("offset",10)
                address_pages = request.GET.get("page",1)
                address = Address.objects.all().filter(client__id=pk)
		if len(address)==0:
			return JsonResponse({'detail':'The user has no saved addresses','petition':'EMPTY'})
		else:
                	paginator = Paginator(address, address_offsets)
                	address_detail = paginator.page(address_pages)
                	serializer = AddressSerializerFull(address_detail, many=True)
                	Paginations = []
                	Paginations.append({'num_pages':paginator.num_pages,'actual_page':address_pages})
                	data = []
                	data.append({'addresses':serializer.data,'pagination':Paginations})
			return Response(data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def mostSoldUser(request,pk):
        try:
                mostSold = extended_order.objects.all().filter(order__user_id=pk,order__status_order_id=4).annotate(image=F('product__product__picture'),price=F('product__base_price'),suggested_price=F('product__product__suggested_price'),name=F('product__product__name'),description=F('product__product__description')).values('product_id','image','price','suggested_price','name','description').annotate(total=Count('product_id')).order_by('-total')[:5]
               
                if(len(mostSold)==0):
                        return JsonResponse({'petition':'EMPTY','detail':'There are no completed orders to calculate the most purchased products'})
                else:
                        return Response(mostSold)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def syncServi(request):
        try:
		storeCode = request.POST.get("storecode",'null')

		if storeCode == 'null':
			return JsonResponse({ 'detail':'servitienda dont sync, the petition no have storecode', 'petition':'DENY'})

		user = User.objects.all().filter(username=storeCode)
		if len(user)==0:
			new_user = User.objects.create_user(storeCode,storeCode,storeCode)
                	new_user.is_active = True
                	new_user.first_name = storeCode
                	new_user.save()
			data = []
			data.append({ 'user':{'id':new_user.id},'store_code':new_user.first_name })
			return Response(data)
		else:
			data = []
			data.append({ 'user':{'id':user[0].id},'store_code':user[0].first_name })
			return Response(data)

        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})
