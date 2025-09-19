from django.shortcuts import render
from rest_framework import viewsets

from cart.models import Cart
from cart.serializers import CartSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Cart"],
    summary="Cart endpoint summary",
    description="Cart Detailed description of what this API does.",
)
class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
