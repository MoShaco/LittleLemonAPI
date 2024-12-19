from rest_framework import serializers
from .models import Category, MenuItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelField):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']