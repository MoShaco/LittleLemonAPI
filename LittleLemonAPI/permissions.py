from rest_framework.permissions import BasePermission
from django.contrib.auth.models import Group


class IsManager(BasePermission):
    def has_permission(self, request, view):
        # Ensure user is authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Check if the user is in 'Manager' group
        return request.user.groups.filter(name='Manager').exists()


class IsDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.groups.filter(name='Delivery Crew').exists()


class IsManagerOrDeliveryCrew(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return request.user.groups.filter(name__in = ['Manager', 'Delivery Crew']).exists()


class IsCustomer(BasePermission):
    """
        Custom permissin to grant access to authenticated users who are not part of specific groups.
    """
    EXCLUDED_GROUPS = ['Manager', 'Delivery Crew']
    
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        return not request.user.groups.filter(name__in = self.EXCLUDED_GROUPS).exists()