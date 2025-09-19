from .models import Category, Product
from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class CategorySerializer(serializers.ModelSerializer):

    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(Category, read_only=True)
    stock_status = serializers.SerializerMethodField()
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"

    @extend_schema_field(serializers.FloatField())
    def get_stock_status(self, obj):
        return obj.stock_status()


class ProductCartSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = ["id", "image_url", "title", "price", "discounted_price"]
