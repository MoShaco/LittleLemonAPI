from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsManager, IsDeliveryCrew, IsManagerOrDeliveryCrew, IsCustomer
from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import CategorySerializer, MenuItemSerializer, CartSerializer, OrderSerializer, OrderItemSerializer
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
    queryset = MenuItem.objects.select_related('category').all()
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


class ManagerUserView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        """
            Get all usres grom Manager group
        """

        manager_group = get_object_or_404(Group, name="Manager")
        manager_users = manager_group.user_set.all()
        data = [{"id": user.id, "username":user.username, "email": user.email} for user in manager_users]
        return Response(data, status=status.HTTP_200_OK)
    
    def post(self, reqeust):
        """
            Add a user to Manager Group
        """

        username = reqeust.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        manager_group = get_object_or_404(Group, name="Manager")

        if user.groups.filter(name="Manager").exists():
            return Response(
                {"message": f"User {username} is already assigned to Manager Group"},
                status=status.HTTP_201_CREATED
                )

        user.groups.add(manager_group)

        return Response(
            {"message": f"User {username} is assigned to Manager Group"},
            status=status.HTTP_201_CREATED
            )
    

    def delete(self, request, pk):
        """
            Delete a user from Manager group
        """
        user = get_object_or_404(User, pk=pk)

        if not user.groups.filter(name="Manager").exclude():
            return Response(
                {"message": f"User {user.username} is not assigned to Manager Group"}, 
                status=status.HTTP_200_OK
                )

        manager_group = get_object_or_404(Group, name="Manager")

        user.groups.remove(manager_group)

        return Response(
            {"message": f"User {user.username} is removed from Manager Group"}, 
            status=status.HTTP_200_OK
            )
    

class DeliveryCrewUserView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        """
            Get all usres grom Delivery Crew group
        """

        delivery_crew_group = get_object_or_404(Group, name="Delivery Crew")
        delivery_crew_users = delivery_crew_group.user_set.all()
        data = [{"id": user.id, "username":user.username, "email": user.email} for user in delivery_crew_users]
        return Response(
            data, 
            status=status.HTTP_200_OK)
    
    def post(self, reqeust):
        """
            Add a user to Delivery Crew Group
        """

        username = reqeust.data.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, username=username)
        delivery_crew_group = get_object_or_404(Group, name="Delivery Crew")

        if user.groups.filter(name="Delivery Crew").exists():
            return Response(
                {"message": f"User {username} is already assigned to Delivery Crew Group"},
                status=status.HTTP_201_CREATED
                )

        user.groups.add(delivery_crew_group)

        return Response(
            {"message": f"User {username} is assigned to Delivery Crew Group"},
            status=status.HTTP_201_CREATED
            )
    

    def delete(self, request, pk):
        """
            Delete a user from Delivery Crew group
        """
        user = get_object_or_404(User, pk=pk)

        if not user.groups.filter(name="Delivery Crew").exclude():
            return Response(
                {"message": f"User {user.username} is not assigned to Delivery Crew Group"}, 
                status=status.HTTP_200_OK
                )

        delivery_crew_group = get_object_or_404(Group, name="Delivery Crew")

        user.groups.remove(delivery_crew_group)

        return Response(
            {"message": f"User {user.username} is removed from Delivery Crew Group"}, 
            status=status.HTTP_200_OK
            )


class CartView(APIView):
    permission_classes =  [IsCustomer]

    def get(self, request):
        items = Cart.objects.filter(user=request.user)
        serialized_items = CartSerializer(items, many=True)
        return Response(serialized_items.data, status=status.HTTP_200_OK)
        
    def post(self, reqeust):
        # Get the current user
        user = reqeust.user

        data = reqeust.data.copy()
        data['user'] = user.id

        serializer = CartSerializer(data=data, context={'request': reqeust})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, reqeust):
        """ Empty the user cart (delete all of the menuitems)"""

        cart_items = Cart.objects.filter(user=reqeust.user)
        if cart_items.exists():
            cart_items.delete()
            return Response({"message": "All items have been deleted from your cart"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Your cart is already empty"}, status=status.HTTP_204_NO_CONTENT)


class OrderView(APIView):
    def get(self, request):
        """ Retrieve orders baesd on user role. """

        user = request.user

        if IsManager().has_permission(request, self):
            orders = Order.objects.all()
        elif IsDeliveryCrew().has_permission(request, self):
            orders = Order.objects.filter(delivery_crew=user)
        else:
            orders = Order.objects.filter(user=user)

        orders = orders.prefetch_related('orderitem_set')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        """ Create an order from the user's cart """

        # Pass the data to OrderSerializer
        serialized_items = OrderSerializer(data={}, context={'request': request})

        # Validate and save
        if serialized_items.is_valid():
            order = serialized_items.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        
        return Response(serialized_items.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_permissions(self):
        permission_classes = []
        if self.request.method == 'GET':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsCustomer]
        return [ permission () for permission in permission_classes]

        

@api_view(['GET'])
@permission_classes([IsCustomer])
def orderItems(request, pk):
    """Retrieve all menu items for a specific order."""
    ...
    # Try to get the order
    order = get_object_or_404(Order, pk=pk)

    # check if the current use is authorized
    if order.user != request.user:
        return Response({'error': 'You are unauthorized to access this order'}, status=status.HTTP_403_FORBIDDEN)
    
    # return the menuietms
    order_items = OrderItem.objects.filter(order=order)
    serialized_items = OrderItemSerializer(order_items, many=True)

    return Response(serialized_items.data, status=status.HTTP_200_OK)