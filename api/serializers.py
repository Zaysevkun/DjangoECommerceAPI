from rest_framework import serializers
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

from api.models import User, Product, Order, ProductsInOrder


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'full_name', 'role', 'mailing_address', 'email')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('pk', 'vendor_code', 'name', 'retail_price', 'purchase_price')


class ProductsInOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductsInOrder
        fields = ('product', 'order', 'quantity')


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ('pk', 'user', 'products')


class CustomAuthTokenSerializer(AuthTokenSerializer):
    username = None
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
