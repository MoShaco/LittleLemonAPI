from rest_framework import serializers
from .models import Category, MenuItem, Cart

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'featured', 'category']
        depth=1

class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(
        source="menuitem.price",
        max_digits=6,
        decimal_places=2,
        read_only=True
        )
    price = serializers.SerializerMethodField()
    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = ['user', 'unit_price', 'price']
    
    def get_price(self, obj):
        """ Calculte the total price """
        return obj.unit_price * obj.quantity
    
    def validate_quantity(self, value):
        """ Validate quantity field"""
        if value < 1:
            raise serializers.ValidationError("Quantity field should be 1 at least")
        return value
    
    def create(self, validated_data):
        """ Handle creation and updating of cart items for the same user and menuitem """
        user = self.context['request'].user
        menuitem = validated_data['menuitem']
        quantity = validated_data['quantity']
        
        existing_cart_item = Cart.objects.filter(user=user, menuitem=menuitem).first()

        # Update the quantity of the menuitem and the price if it's exists
        if existing_cart_item:
            existing_cart_item.quantity += quantity
            existing_cart_item.price = existing_cart_item.quantity * existing_cart_item.unit_price
            existing_cart_item.save()
            return existing_cart_item
        
        # Cretate a new record
        validated_data['user'] = user
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = quantity * menuitem.price
        return super().create(validated_data)