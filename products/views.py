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
from django.core.paginator import Paginator
from django.db.models import F,Sum,Count,Max
from django.core.serializers.json import DjangoJSONEncoder
from shopkeepers.models import inventory

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
                inventoriesS = product.objects.all().annotate(categoryid=F('subcategory__category_id'),name_category=F('subcategory__category__name'),pictures=F('subcategory__category__picture')).values('categoryid','name_category','pictures').annotate(totalProductsinCategory=Count('id')).order_by('-totalProductsinCategory')

                subcategories = product.objects.all().annotate(categoryid=F('subcategory__category_id'),subcategoryid=F('subcategory_id'),name_subcategory=F('subcategory__name')).values('categoryid','subcategoryid','name_subcategory').annotate(totalProd=Count('subcategoryid'))
                for x in inventoriesS:
                        x.update({'subcategories':[]})
                for y in subcategories:
                        for z in inventoriesS:
                                if z['categoryid'] == y['categoryid']:
                                        z['subcategories'].append({'name':y['name_subcategory'],'id':y['subcategoryid'],'total':y['totalProd']})
                categorias = json.dumps(list(inventoriesS), cls=DjangoJSONEncoder)
                return Response(inventoriesS)

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

@api_view(['POST'])
#@permission_classes((permissions.AllowAny,))
def getProductsAllList(request):
        #if request.method == "GET":
        #        products = product.objects
        #        serializer = ProductSerializersWithImage(products, many=True)
        #        return Response(serializer.data)
        #if request.method == "POST":
        try:
                offsets = request.POST.get("offset",10)
                pages = request.POST.get("page",1)
                subcategory = request.POST.get("subcategory",False)
                category = request.POST.get("category",False)
                store_id = request.POST.get("store_id",False)
                if( (category is not False) and (subcategory is False) ):
                        productList = product.objects.all().filter(subcategory__category_id=category)
                if( (subcategory is not False) and (category is False) ):
                        productList = product.objects.all().filter(subcategory_id=subcategory)
                if( (category is False) and (subcategory is False) ):
                        productList = product.objects.all()
                paginator = Paginator(productList, offsets)
                products_detail = paginator.page(pages)
                serializer = ProductSerializersWithImage(products_detail, many=True)
                if store_id is not False:
                        for x in serializer.data:
                                inventoryShop = inventory.objects.all().filter(shop_id=store_id,product_id=x['id'])
                                if len(inventoryShop)!=0:
                                        x.update({'in_shop':True,'price_in_shop':inventoryShop[0].base_price})
                                else:
                                        x.update({'in_shop':False})
                Paginations = []
                Paginations.append({'num_pages':paginator.num_pages,'actual_page':pages})
                data = []
                data.append({'inventory':serializer.data,'pagination':Paginations})
                return Response(data)
        except Exception as e:
                return JsonResponse({"petition":"ERROR","detail":e})


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
		if 'image' not in request.FILES:
			image = "null"
		else:
			image = request.FILES['image']

		if request.POST.get("product_id") is None:
			return JsonResponse({"petition":"EMTPY","detail":"The product_id can not be null"})

		p = product.objects.filter(pk = request.POST.get("product_id"))

		if request.POST.get("name") is not None:
			p.update(name=request.POST.get("name"))

		if request.POST.get("suggested_price") is not None:
			p.update(suggested_price=request.POST.get("suggested_price"))

		if request.POST.get("suggested_price") is not None:
			p.update(description=request.POST.get("description"))

		if image is not "null":
			imagePath = '/webapps/hello_django/server-tiendosqui/misitio/'+image.name
			destination = open(imagePath, 'wb+')
			for chunk in image.chunks():
				destination.write(chunk)
				destination.close()

			p.update(picture = image)
		return JsonResponse({"petition":"OK","detail":"The product was successfully changed"})

	except Exception as e:
		return JsonResponse({"petition":"ERROR","detail":e})

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

