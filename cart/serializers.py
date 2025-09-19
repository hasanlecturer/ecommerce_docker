from rest_framework import serializers
from cart.models import CartItem
from products.serializers import ProductCartSerializer
from drf_spectacular.utils import extend_schema_field


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    sub_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "sub_total", "total"]

    @extend_schema_field(serializers.FloatField())
    def get_total(self, obj):
        return obj.product.price * obj.quantity

    @extend_schema_field(serializers.FloatField())
    def get_sub_total(self, obj):
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    sub_total = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )
    total = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    total_discount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    session_key = serializers.CharField(read_only=True)
    is_anonymous = serializers.BooleanField(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "session_key",
            "is_anonymous",
            "items",
            "total_items",
            "sub_total",
            "total",
            "total_discount",
        ]
