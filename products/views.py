from django.shortcuts import render

from products.pagination import ProductPagination
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema
from django_filters.rest_framework import DjangoFilterBackend
from .filters import ProductFilter


@extend_schema(
    tags=["Category"],
    summary="Category endpoint summary",
    description="Category Detailed description of what this API does.",
)
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = "slug"


@extend_schema(
    tags=["Products"],
    summary="Product endpoint summary",
    description="Product Detailed description of what this API does.",
)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    lookup_field = "slug"
    ordering_fields = ["name", "price", "created_at"]
    filterset_class = ProductFilter
    pagination_class = ProductPagination

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)
        return queryset
