from django.urls import path
from . import views


urlpatterns = [
    path('categories', views.CategoriesView.as_view(), name="categories"),
    path('categories/<int:pk>', views.CategoryView.as_view(), name="category"),
    path('menu-items', views.MenuItemsView.as_view(), name='menuitems'),
    path('menu-items/<int:pk>', views.MenuItemView.as_view(), name='manuitem'),
    path('groups/manager/users', views.ManagerUserView.as_view(), name="Managers"),
    path('groups/manager/users/<int:pk>', views.ManagerUserView.as_view(), name="Manager"),
    path('groups/delivery-crew/users', views.DeliveryCrewUserView.as_view(), name="Delivery Crews"),
    path('groups/delivery-crew/users/<int:pk>', views.DeliveryCrewUserView.as_view(), name="Delivery Crew"),
]