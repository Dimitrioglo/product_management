from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    wished_by = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sku', 'price', 'description', 'wished_by']