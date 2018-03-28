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
from users.models import Profile
from .serializers import *
from users.serializers import ProfileSerializer
from django.core.paginator import Paginator
from django.db.models import Sum,Max,Count,Avg
import json
import requests
import time
from django.conf import settings
from fcm_django.models import FCMDevice
'''
def loginAgendaServi():
	url = 'http://scheduler5.sitidoctor-161813.appspot.com/api/auth/login'
	data ='{"username":"manuel.pelaez", "password":"CvJaYD3oM8q529XUor","client_secret":"A8jP3Ktr0mzX"}'
	responses = requests.post(url, data=data)
	r = responses.json()
	return Response(r['data']['authorization']['access_token'])

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def createEventsAgenda(request): #dataAgenda,EngineerId):
	login = requests.post('http://scheduler5.sitidoctor-161813.appspot.com/api/auth/login',data='{"username":"manuel.pelaez", "password":"CvJaYD3oM8q529XUor","client_secret":"A8jP3Ktr0mzX"}')
	rlogin =login.json()
	hash = rlogin #['data']['authorization']['access_token']
	return Response(hash)
	token = 'Bearer G0LUMaCvblhWaDQKdnIcmchiAbY8cU' #hash
	url = 'http://scheduler5.sitidoctor-161813.appspot.com/api/v1/events/create'
	dataAgenda =' "description": "support task","description_id": 999,"init_date": "2018-03-26","end_date": "2018-03-26","init_hour": "11:00","end_hour": "13:00","latitude": null,"longitude": null,"repeat": "ALLDAY","address":"bogota","city":"bogota","ghost": false'
	EngineerId = 1
	data = '{"user_id":'+str(EngineerId)+',"timezones":[{'+ dataAgenda +'}] }'
	header = {"Authorization":token.encode("ascii", "ignore")}
	responses = requests.post(url, headers=header, data=data)
	r = responses.json()
	return Response(r)
'''
@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def TaskCreate(request):
	try:
		data = json.loads(request.body)

		taskNew = task(
			client_id_id = data["client_id"],
			date = data["date"],
			startTime = data["startTime"],
			address = data["address"],
			address_details = data["address_details"],
			lat =data["lat"],
			lng=data["lng"],
			city=data["city"],
			activity_id_id=data["activity_id"],
			job_description=data["job_description"],
			notes_engineer=data["notes_engineer"],
			required_testing=data["required_testing"],
			site_contact=data["site_contact"],
			site_contact_number=data["site_contact_number"],
			status_id=1
		)
		taskNew.save()
		#with SocketIO('apitest.pediidos.com', 9090, LoggingNamespace) as socketIO:
                #	socketIO.emit('task','{"xx":"xx"}') #notification)
                #	socketIO.wait(seconds=1)
		#pusher_client.trigger('my-channel', 'my-event', {'message': 'hello world'})
		return JsonResponse({'detail':taskNew.id,'petition':'ok'})
	except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def TaskAssign(request):
        try:
                data = json.loads(request.body)
		idTask = data["task_id"]
		idEngi = data["engineer_id"]
		validEngineer = User.objects.all().filter(pk=idEngi)
		if validEngineer[0].is_staff == False:
			return JsonResponse({'detail':'this user is not an engineer','petition':'DENY'})

		taskNotExist = taskExtend.objects.all().filter(task_id=idTask)
		#agregar validacion de agendamient
                if len(taskNotExist)==0:
			taskExtend(
                        	task_id = idTask,
                        	engineer_id = idEngi
                	).save()
			#task.objects.all().filter(pk=idTask).update(status_id=2)
			saveTask =task.objects.all().filter(pk=idTask).update(status_id=2)

			historytask = taskTrackingStatus(
				task_id = idTask,
				status_id = 2
			).save()
			#data =' "description":"task new", "description_id": 99999, "init_date":' +saveTask[0].date+ ', "end_date":' +saveTask[0].date+ ', "init_hour":' +saveTask[0].startTime+ ', "end_hour":' +saveTask[0].startTime+ ', "latitude":' +saveTask[0].lat+ ', "longitude":' +saveTask[0].lng+ ' ,"repeat": "ALLDAY", "address":' +saveTask[0].address+ ' ,"city":' +saveTask[0].city+ ' ,"ghost": false'
			#createEventsAgenda(data,idEngi)

                	return JsonResponse({'detail':'task successfully assigned to the engineer','petition':'OK'})
		else:
			return JsonResponse({'detail':'The task already exists and was assigned to: ' + taskNotExist[0].engineer.first_name + " " +taskNotExist[0].engineer.last_name ,'petition':'DENY'})
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def TaskChangeStatus(request):
        try:
                data = json.loads(request.body)
                idTask = data["task_id"]
                idStatus = data["status_id"]

                taskExist = taskExtend.objects.all().filter(task_id=idTask) #, task__status_id=1)

                if len(taskExist)>0:
                        saveTask =task.objects.all().filter(pk=idTask).update(status_id=idStatus)

                        historytask = taskTrackingStatus(
                                task_id = idTask,
                                status_id = idStatus
                        ).save()
                        return JsonResponse({'detail':'Task changes status successfully','petition':'OK'})
                else:
                        return JsonResponse({'detail':'The task_id of the task does not exist or is not available to change','petition':'DENY'})
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def ActivitiesAll(request):
        try:
                activitiesAlls = activities.objects.all()
		serializer = activitiesSerializer(activitiesAlls, many=True)
                return Response(serializer.data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def taskGetOne(request,pk):
        try:
                taskOne = task.objects.all().filter(pk=pk)
                serializer = taskStatusSerializer(taskOne, many=True)
                return Response(serializer.data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def TaskPendingAll(request):
        try:
		user = request.GET.get("user_id","null")
		#return Response(user)
		if user is not "null":
			taskAlls = task.objects.all().filter(client_id_id=user,status_id=1) #status id 1 = pending
		else:
                	taskAlls = task.objects.all().filter(status_id=1) #status id 1 = pending
                serializer = taskStatusSerializer(taskAlls, many=True)
                return Response(serializer.data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def taskEngineer(request):
        try:
                user = request.GET.get("user_id","null")
                calendar = request.GET.get("calendar","null")

                if user is not "null":
                        taskAlls = taskExtend.objects.all().filter(engineer_id=user) #,status_id=1) #status id 1 = pending
                else:
                        taskAlls = taskExtend.objects.all() #.filter(status_id=1) #status id 1 = pending

                serializer = taskEngineerSerializer(taskAlls, many=True)
		agenda = []
		if calendar == "true":
			for x in serializer.data:
				if x["task"]["date"][0:4] == "2018":
					fecha = x["task"]["date"]
				else:
					fecha = x["task"]["date"][6:10] +"-" +x["task"]["date"][3:5]+"-"+x["task"]["date"][0:2] 
				#return Response(fecha)
				agenda.append({"address": x["task"]["address"],"city": x["task"]["city"],"date_prog": fecha,"description": x["task"]["activity_id"]["name"],"description_id": "99999","end_hour": x["task"]["startTime"],"ghost": "false","id": x["task"]["id"],"init_hour": x["task"]["startTime"],"latitude": x["task"]["lat"],"longitude": x["task"]["lng"],"schedstatus_id": x["task"]["status"]["id"]})
                	return Response(agenda)

		else:
			return Response(serializer.data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

#@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
#def QualifyShop(request):
#	try:
#		data = json.loads(request.body)
#		if data["order_id"] is None:
#			return JsonResponse({'petition':'EMPTY','detail':'the field order_id does not null'})
#
#		user =  Orders.objects.all().filter(pk=data["order_id"])
#		if len(user)==0:
#			return JsonResponse({'petition':'EMPTY','detail':'You can not qualify an order that does not exist'})
#		else:
#			qualify =qualifications_shop.objects.all().filter(shop_id= user[0].shop_id).aggregate(Sum('rate'),Count('id'))#.get('rate__sum')
#			q = qualify["rate__sum"]/qualify["id__count"]
#			return JsonResponse(round(q, 1),safe=False)
#			TotalQualify = len(qualify)
#		return JsonResponse({'detail':'The buyer was successfully qualified','petition':'OK'})
#	except Exception as e:
#               return JsonResponse({"petition":"ERROR","detail":e})


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def registerUsers(request):
        if request.method == "POST":
                user = json.loads(request.body)
                if len(user["email"])==0:
                        return JsonResponse({'petition':'EMTPY','detail':'Fields can not be empty'})
                try:
                        new_user = User.objects.create_user(user["email"],user["email"],user["password"])
                        if(user["type"]==1):
				new_user.is_active = True
			else:
				new_user.is_active = True #cambiar a False
				new_user.is_staff = True #cambiar a False

                        new_user.first_name = user["first_name"]
			new_user.last_name = user["last_name"]
                        new_user.save()
			if(user["type"]==1):
                        	profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=user["type"], status_id=1) # activate customer
                        else:
				profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=user["type"], status_id=1) #change to 2  #pending engineer
			profile_user.save()
			return JsonResponse({'detail':'the user has been created','petition':'OK'})
                except Exception as e:
                        return JsonResponse({'petition':'DENY','detail':e})#'user already exists' })

@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def deviceusers(request):
        try:
                data = json.loads(request.body)
                fcm = FCMDevice.objects.all().filter(user_id=data["userid"])
                if len(fcm)==0:
                        fcm1 = FCMDevice(registration_id=data["users_deviceid"],user_id=data["userid"],name="usuario",type=data["type_device"])
                        fcm1.save()
                        return JsonResponse({'petition':'OK','detail':'The deviceID was created on the server'})
                else:
                        fcm[0].registration_id=data["users_deviceid"]
                        fcm[0].save()
                        return JsonResponse({'petition':'OK','detail':'The DeviceID was updated'})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def usersAll(request):
        try:
		type= request.GET.get("type")
		if type=="engineer":
			activitiesAlls = Profile.objects.all().filter(type_user__name="Engineer")
		elif type=="user":
			activitiesAlls = Profile.objects.all().filter(type_user__name="Customer")
		else:
			activitiesAlls = Profile.objects.all()
                serializer = ProfileSerializer(activitiesAlls, many=True)
                return Response(serializer.data)
        except Exception as e:
               return JsonResponse({"petition":"ERROR","detail":e.message})

