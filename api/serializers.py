from rest_framework import serializers
from api.models import User, Product, Order


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'full_name', 'role', 'mailing_address', 'email')


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('vendor_code', 'name', 'retail_price', 'purchase_price')


class OrderSerializer(serializers.ModelSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, queryset=Product.objects.all())

    class Meta:
        model = Order
        fields = ('user', 'products')

    def partial_update(self, validated_data):
        request = self.context.get('request', None)
        current_user = request.user
        obj, created = Order.objects.get_or_create(user=current_user)
        obj.products.add(validated_data.get('product'))
        return obj
