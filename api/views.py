from rest_framework import viewsets, permissions, mixins, views
from rest_framework.authtoken.views import ObtainAuthToken
import wkhtmltopdf
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response

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


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]

    def put(self, request, format=None):
        file_obj = request.data['file']
        products = file_obj.readlines()
        for product in products[1:]:
            product = product.decode('utf-8').strip('\n')
            product_values = product.split(";")
            Product.objects.create(vendor_code=product_values[0],
                                   name=product_values[1],
                                   retail_price=product_values[2])
        return Response(status=204)


# def pdf_checkout(request):
#     pdf = wkhtmltox.Pdf()
#     pdf.set_global_setting('out', 'two.pdf')
#     pdf.add_page({'page': 'http://www.tweakers.net'})
#     pdf.convert()
