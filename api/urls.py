from django.contrib import admin
from django.urls import path
from rest_framework import routers
from .views import UserViewSet, ProductViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [

]