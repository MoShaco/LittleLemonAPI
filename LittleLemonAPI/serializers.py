import datetime
from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem

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
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']
        read_only_fields = ['user', 'total', 'date']
    
    def validate(self, data):
        # Query for carts 
        user = self.context['request'].user
        existing_cart = Cart.objects.filter(user=user)
        if not existing_cart:
            raise serializers.ValidationError(f"The cart of the user {user.username} is empty")
        
        return data

    def create(self, validated_data):
       
       # Get the current user
       user = self.context['request'].user

       # Create an order
       order = Order.objects.create(
           user=user,
           total=0,
           date=datetime.date.today(),
       )

       # Create orderitems
       total = 0
       cart_items = Cart.objects.filter(user=user)

       for item in cart_items:
           OrderItem.objects.create(
               order=order,
               menuitem=item.menuitem,
               quantity=item.quantity,
               unit_price=item.unit_price,
               price=item.price
           )
           total += item.price
       # Update the order total price
       order.total = total
       order.save()
       
       # Delete the cart
       cart_items.delete()

       return order
    
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['id', 'menuitem', 'quantity', 'unit_price', 'price']
    

    def get_menuitem(self, obj):
        menuitem_data = {
            'id': obj.menuitem.id,
            'title': obj.menuitem.title,
            'category': {
                'id': obj.menuitem.category.id,
                'title': obj.menuitem.category.title,
                'slug': obj.menuitem.category.slug
            }
        
        }
        return menuitem_data