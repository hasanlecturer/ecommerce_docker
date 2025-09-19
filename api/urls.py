from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from products.views import CategoryViewSet, ProductViewSet
from cart.views import CartViewSet
from orders.views import OrderView, OrderItemView
from .views import ChatBotView

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderView, basename='order')
router.register(r'order-items', OrderItemView, basename='order-item')



urlpatterns = [
    
    # Rest API URLs
    path('customer/', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("chatbot/", ChatBotView.as_view(), name="chatbot"),
    # Optional UI:
    path(
        "",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    )
] + router.urls
