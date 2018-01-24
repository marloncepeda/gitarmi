# -*- encoding: utf-8 -*-
from .models import *
from .serializers import *
from rest_framework import viewsets
from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import filters
#from .filters import *

class UsersViewsets(viewsets.ModelViewSet):
    serializer_class = UsersSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny,]

class StatusViewsets(viewsets.ModelViewSet):
    serializer_class = StatusSerializer
    queryset = Status.objects.all()

class TypesViewsets(viewsets.ModelViewSet):
    serializer_class = TypesSerializer
    queryset = Types.objects.all()
    #permission_classes = [permissions.AllowAny,]
#    filter_backends = (filters.DjangoFilterBackend,filters.SearchFilter,)
#    search_fields = ('username',)

class DevicesViewsets(viewsets.ModelViewSet):
    serializer_class = DevicesSerializer
    queryset = Devices.objects.all()

class WithoutShopsViewsets(viewsets.ModelViewSet):
    serializer_class = WithoutShopsSerializer
    queryset = Without_shops.objects.all()

class AddressViewsets(viewsets.ModelViewSet):
    serializer_class = AddressSerializerFull
    queryset = Address.objects.all()
