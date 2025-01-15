from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['amazon_code', 'name', 'price', 'rating', 'reviews_count']
