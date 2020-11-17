from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import ProductViewSet, OrderViewSet, CustomAuthToken, ProductsInOrderViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order_products', ProductsInOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]
