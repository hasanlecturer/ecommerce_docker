from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("", include("user_accounts.urls")),
    path("", include("cart.urls")),
    path("", include("orders.urls")),
    path("", include("products.urls")),
]
