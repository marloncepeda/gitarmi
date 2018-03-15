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
			task.objects.all().filter(pk=idTask).update(status_id=2)
			historytask = taskTrackingStatus(
				task_id = idTask,
				status_id = 2
			)
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

		validEngineer = User.objects.all().filter(pk=idEngi)

                if validEngineer[0].is_staff == False:
                        return JsonResponse({'detail':'this user is not an engineer','petition':'DENY'})

                taskNotExist = taskExtend.objects.all().filter(task_id=idTask, task__status_id=1)

                if len(taskNotExist)==0:
                        taskExtend(
                                task_id = idTask,
                                engineer_id = idEngi
                        ).save()
                        task.objects.all().filter(pk=idTask).update(status_id=2)
                        historytask = taskTrackingStatus(
                                task_id = idTask,
                                status_id = 2
                        )
                        return JsonResponse({'detail':'task successfully assigned to the engineer','petition':'OK'})
                else:
                        return JsonResponse({'detail':'The task already exists and was assigned to:','petition':'DENY'})
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
                serializer = taskSerializer(taskOne, many=True)
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
				new_user.is_active = False

                        new_user.first_name = user["first_name"]
			new_user.last_name = user["last_name"]
                        new_user.save()
			if(user["type"]==1):
                        	profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=user["type"], status_id=1) # activate customer
                        else:
				profile_user = Profile(user_id=new_user.id,phone=user["phone"],type_user_id=user["type"], status_id=2) #pending engineer
			profile_user.save()
			return JsonResponse({'detail':'the user has been created','petition':'OK'})
                except Exception as e:
                        return JsonResponse({'petition':'DENY','detail':e})#'user already exists' })
