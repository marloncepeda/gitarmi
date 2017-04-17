# -*- encoding: utf-8 -*-
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import filters
#from .filters import *

class TypesViewsets(viewsets.ModelViewSet):
    serializer_class = TypesSerializer
    queryset = types.objects.all()
    #permission_classes = [permissions.AllowAny,]
#    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
#    search_fields = ('username',)

class statuViewsets(viewsets.ModelViewSet):
    serializer_class = statuSerializers
    queryset = statu.objects.all()

class InfoShopViewsets(viewsets.ModelViewSet):
    serializer_class = InfoShopSerializers
    queryset = info.objects.all()

class StateViewsets(viewsets.ModelViewSet):
    serializer_class = StateSerializers
    queryset = state.objects.all()

class TypeDeliveriesViewsets(viewsets.ModelViewSet):
    serializer_class = TypeDeliveriesSerializers
    queryset = types_deliveries.objects.all()

class PriceDeliveryViewsets(viewsets.ModelViewSet):
    serializer_class = PriceDeliverySerializers
    queryset = price_delivery.objects.all()