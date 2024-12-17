from django.urls import path
from . import views


urlpatterns = [
    path('categories', views.CategoriesView.as_view(), name="categories"),
    path('categories/<int:pk>', views.CategoryView.as_view(), name="category"),
]