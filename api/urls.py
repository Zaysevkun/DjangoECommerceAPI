from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .tasks import create_pdf
from .views import ProductViewSet, OrderViewSet, CustomAuthToken, ProductsInOrderViewSet, FileUploadView

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'order_products', ProductsInOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('file_upload/', FileUploadView.as_view()),
    path('checkout_pdf/', create_pdf),
    path('token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]
