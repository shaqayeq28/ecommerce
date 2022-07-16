from rest_framework import serializers

from inventory.models import Product
from accounts.models import Supplier


class SupplierSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = ['company_name']


class ProductListSerializer(serializers.ModelSerializer):

    supplier = SupplierSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'supplier']


class ProductDetailSerializer(serializers.ModelSerializer):

    supplier = SupplierSerializer(many=True)

    class Meta:
        model = Product
        fields = ('supplier', 'product_name', 'product_price',
                  'rate', 'available_quantity', 'image', 'description')
