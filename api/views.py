from django.shortcuts import render
from rest_framework import viewsets, permissions
from .serializers import UserSerializer, OrderSerializer, ProductSerializer
from .models import User, Product, Order
from .permissions import OrderPermissions


# ViewSet for interacting with Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ViewSet for interacting with Orders
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (OrderPermissions, permissions.IsAuthenticated)

