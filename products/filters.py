from django_filters import rest_framework as filters
from .models import Product


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = filters.NumberFilter(field_name="price", lookup_expr="lte")
    in_stock = filters.BooleanFilter(method="filter_in_stock")

    class Meta:
        model = Product
        search_fields = ["title", "description", "category__name"]
        ordering_fields = ["name", "price", "created_at"]
        ordering = ["-created_at"]
        fields = {
            "category__slug": ["exact"],
            "category__name": ["exact", "icontains"],
            "price": ["gte", "lte"],
        }

    def filter_in_stock(self, queryset, name, value):
        if value:  # true → stock > 0
            return queryset.filter(stock__gt=0)
        return queryset.filter(stock__lte=0)
