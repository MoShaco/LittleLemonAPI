from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsManager, IsDeliveryCrew, IsManagerOrDeliveryCrew
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
# Create your views here.


class CategoriesView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [ permission () for permission in permission_classes]


class CategoryView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [ permission () for permission in permission_classes]

class MenuItemsView(generics.ListCreateAPIView):
    queryset = MenuItem
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [permission() for permission in permission_classes]


class MenuItemView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem
    serializer_class = MenuItemSerializer

    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsManager]
        return [ permission() for permission in permission_classes]
