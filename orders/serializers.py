from rest_framework import serializers
from common.helper_serializers import BaseAddressSerializer
from .models import Order, OrderItem, ShippingAddress, BillingAddress
from drf_spectacular.utils import extend_schema_field


class ShippingAddressSerializer(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        model = ShippingAddress
        fields = [
            "full_name",
            "street_address",
            "apartment",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
        ]


class BillingAddressSerializer(BaseAddressSerializer):
    class Meta(BaseAddressSerializer.Meta):
        model = BillingAddress
        fields = [
            "full_name",
            "street_address",
            "apartment",
            "city",
            "state",
            "postal_code",
            "country",
            "phone",
        ]


class OrderItemSerializers(serializers.ModelSerializer):
    product_title = serializers.CharField(source="product.title", read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ["id", "product_title", "quantity", "price", "total_price"]
        read_only_fields = ["id", "price", "total_price"]

    @extend_schema_field(serializers.FloatField())
    def get_total_price(self, obj):
        return obj.total_price


class OrderSerializer(serializers.ModelSerializer):
    shipping_address = ShippingAddressSerializer()
    billing_address = BillingAddressSerializer()
    items = OrderItemSerializers(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "order_number",
            "status",
            "total_amount",
            "shipping_address",
            "billing_address",
            "items",
        ]
        read_only_fields = ["order_number", "created_at", "updated_at"]

    def create(self, validated_data):
        shipping_data = validated_data.pop("shipping_address")
        billing_data = validated_data.pop("billing_address")
        items_data = validated_data.pop("items")

        shipping_address = ShippingAddress.objects.create(**shipping_data)
        billing_address = BillingAddress.objects.create(**billing_data)

        order = Order.objects.create(
            shipping_address=shipping_address,
            billing_address=billing_address,
            **validated_data
        )

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
