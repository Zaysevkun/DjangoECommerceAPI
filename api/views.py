from rest_framework import viewsets, permissions, mixins, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializers import OrderSerializer, ProductSerializer, CustomAuthTokenSerializer, ProductsInOrderSerializer
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.schemas import ManualSchema
from .models import Product, Order, ProductsInOrder
from .permissions import OrderPermissions


class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="email",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Email",
                        description="Valid email for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )


# ViewSet for interacting with Products
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# ViewSet for interacting with Orders
class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (OrderPermissions, permissions.IsAuthenticated)


class ProductsInOrderViewSet(mixins.CreateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = ProductsInOrder.objects.all()
    serializer_class = ProductsInOrderSerializer
    permission_classes = (OrderPermissions, permissions.IsAuthenticated)


