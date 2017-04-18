from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, generics, filters
from rest_framework.generics import RetrieveAPIView
from .models import *
from .serializers import *
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json

# Create your views here.

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getCategoryOneToOne(request,pk):
	if request.method == "GET":
		categoryes = category.objects.filter(pk=pk)
		serializer =  CategorySerializer(categoryes, many=True)
		return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getCategoryAll(request):
        if request.method == "GET":
                categoryes = category.objects
                serializer =  CategorySerializer(categoryes, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getSubategoryAll(request):
        if request.method == "GET":
                subcategoryes = subcategory.objects
                serializer = SubcateorySerializer(subcategoryes, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getSubcategoryOneToOne(request,pk):
        if request.method == "GET":
                subcategoryes = subcategory.objects.filter(category=pk)
                serializer =  SubcateorySerializer(subcategoryes, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getProductsOneToOne(request,pk):
        if request.method == "GET":
                subcategoryes = product.objects.filter(subcategory=pk)
                serializer = ProductSerializersWithImage(subcategoryes, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getProductsAll(request,pk):
        if request.method == "GET":
                products = product.objects.filter(subcategory=pk)
                serializer = ProductSerializersWithImage(products, many=True)
                return Response(serializer.data)

@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getProductsAllList(request):
        if request.method == "GET":
                products = product.objects
                serializer = ProductSerializersWithImage(products, many=True)
                return Response(serializer.data)


@api_view(['GET'])
#@permission_classes((permissions.AllowAny,))
def getProductsAllCategory(request,pk):
        if request.method == "GET":
                products = product.objects.filter(subcategory__category=pk)
                serializer = ProductSerializersWithImage(products, many=True)
                return Response(serializer.data)

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def addProduct(request):
	try:
		nameProduct = request.POST.get("product_name")
		priceProduct = request.POST.get("product_price")
		descriptionProduct = request.POST.get("product_description")
		pictureProduct = request.FILES["product_picture"]
		subcategory = request.POST.get("subcategory_id")
                if(len(nameProduct)==0)or(len(priceProduct)==0)or(len(pictureProduct)==0):
                        JsonResponse({'petition':'DENY','detail':'The product_(Fields) field can not be empty'})
                else:
                        newProduct = product(name=nameProduct,subcategory_id=subcategory,suggested_price=priceProduct,description=descriptionProduct,picture=pictureProduct)
                        newProduct.save()
                        return JsonResponse({'petition':'OK','detail':'Product created successfully'})
	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['PUT'])
#@permission_classes((permissions.AllowAny,))
#@staff_member_required 
def suspendActivateProduct(request):#, username):    
    try:
        p = product.objects.get(pk = request.POST["product_id"])
        if(request.POST["status"]=="Suspender"):
                p.status = False
		p.save()
                return JsonResponse({"petition":"OK","detail":"The product is suspended"})
        elif(request.POST["status"]=="Activar"):
                p.status = True
		p.save()
                return JsonResponse({"petition":"OK","detail":"The product is activated"})
        else:
                return JsonResponse({"petition":"EMTPY","detail":"The fields status is not null"})
    except product.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})

    except Exception as e:
        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['PUT'])
#@permission_classes((permissions.AllowAny,)) 
def editProductGlobal(request):   
    try:
        if( (len(request.POST["product_id"])>0)or(len(request.POST["name"])>0)or(len(request.POST["suggested_price"])>0)or(len(request.POST["description"])>0)):
                p = product.objects.filter(pk = request.POST["product_id"])
		p.update(name=request.POST["name"],suggested_price=request.POST["suggested_price"],description=request.POST["description"])
                return JsonResponse({"petition":"OK","detail":"The product was successfully changed"})
        else:
                return JsonResponse({"petition":"EMTPY","detail":"The fields status is not null"})
    except product.DoesNotExist:
        return JsonResponse({"petition":"DENY","detail":"User does not exist"})

    except Exception as e:
        return JsonResponse({"petition":"ERROR","detail":e.message})

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def searchProductGlobal(request):
        try:
                data = json.loads(request.body)
                if(len(data["search"])==0):
                        return Response({'petition':'EMTPY','detail':'The fields search not null'})
                try:
                        products = product.objects.all().filter(name__unaccent__icontains=data["search"],status=True)
                        serializer = ProductSerializersWithImage(products, many=True)
                        if (len(products)>0):
                                return Response(serializer.data)
                        else:
                                return Response({'petition':'OK','detail':'The products you are looking for do not exist'})
                except:
                        return JsonResponse({'petition':'DENY','detail':'the fields extra dont have data'})
	except product.DoesNotExist:
        	return JsonResponse({"petition":"DENY","detail":"The product does not exist"})

 	except Exception as e:
        	return JsonResponse({"petition":"ERROR","detail":e.message})

'''@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def addMultipleProduct(request):
        try:
		data = json.loads(request.body)
                newProduct = product(name=nameProduct,subcategory_id=subcategory,suggested_price=priceProduct,description=descriptionProduct,picture=picturePro$
		newProduct.save()
                return JsonResponse({'petition':'OK','detail':'Product created successfully'})
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e.message})'''

