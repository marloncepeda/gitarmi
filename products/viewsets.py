# -*- encoding: utf-8 -*-
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import filters
#from .filters import *

class CategoryViewsets(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = category.objects.all()

class SubcategoryViewsets(viewsets.ModelViewSet):
    serializer_class = SubcateorySerializer
    queryset = subcategory.objects.all()

class ProductFullViewsets(viewsets.ModelViewSet):
    serializer_class = ProductSerializersFull
    queryset = product.objects.all()