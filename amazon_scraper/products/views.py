from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Product
from .utils import scrape_amazon

class ProductAPI(APIView):
    def get(self, request):
        amazon_code = request.query_params.get('code')
        if not amazon_code:
            return Response({"error": "Amazon code is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check cache
        cached_data = cache.get(amazon_code)
        if cached_data:
            return Response(cached_data)

        # Check database
        try:
            product = Product.objects.get(amazon_code=amazon_code)
            data = {
                "name": product.name,
                "price": product.price,
                "rating": product.rating,
                "reviews_count": product.reviews_count,
            }
            cache.set(amazon_code, data, timeout=3600)
            return Response(data)
        except Product.DoesNotExist:
            # Scrape data if not found
            scraped_data = scrape_amazon(amazon_code)
            if not scraped_data:
                return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

            # Save to DB and cache
            product = Product.objects.create(**scraped_data)
            cache.set(amazon_code, scraped_data, timeout=3600)
            return Response(scraped_data)
