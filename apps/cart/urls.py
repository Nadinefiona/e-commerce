from django.urls import path

from apps.cart.views import CartDetailAPIView, CartItemAPIView

urlpatterns = [
    path("", CartDetailAPIView.as_view(), name="cart-detail"),
    path("items/", CartItemAPIView.as_view(), name="cart-items"),
]
