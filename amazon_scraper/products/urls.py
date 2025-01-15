from django.urls import path
from .views import ProductAPI

urlpatterns = [
    path('api/product/', ProductAPI.as_view(), name='product_api'),
]
