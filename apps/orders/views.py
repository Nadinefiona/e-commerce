import logging

from django.db import transaction
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.models import User
from apps.cart.models import Cart
from apps.orders.models import Order, OrderItem
from apps.orders.serializers import OrderSerializer

logger = logging.getLogger(__name__)


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ["status"]
    ordering = ["-created_at"]
    http_method_names = ["get", "post", "patch"]

    def get_queryset(self):
        qs = Order.objects.select_related("user").prefetch_related("items__product")
        if self.request.user.role == User.Role.ADMIN or self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        shipping_address = request.data.get("shipping_address", "").strip()
        if not shipping_address:
            return Response({"detail": "Please provide a shipping address."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
        except Cart.DoesNotExist:
            return Response({"detail": "Your cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

        cart_items = cart.items.select_related("product").all()
        if not cart_items.exists():
            return Response({"detail": "Your cart is empty. Add items before placing an order."}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user, shipping_address=shipping_address)
        total = 0

        for item in cart_items:
            if item.quantity > item.product.stock:
                transaction.set_rollback(True)
                return Response(
                    {"detail": f"Sorry, only {item.product.stock} units of '{item.product.name}' are available."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            OrderItem.objects.create(
                order=order,
                product=item.product,
                product_name=item.product.name,
                price=item.product.price,
                quantity=item.quantity,
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])
            total += item.product.price * item.quantity

        order.total_amount = total
        order.save(update_fields=["total_amount"])
        cart.items.all().delete()

        logger.info("Order %s created for user %s (total: %s)", order.id, request.user.username, total)
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        if request.user.role != User.Role.ADMIN and not request.user.is_staff:
            return Response({"detail": "Only admins can update order status."}, status=status.HTTP_403_FORBIDDEN)

        order = self.get_object()
        new_status = request.data.get("status")
        valid = {c[0] for c in Order.Status.choices}
        if new_status not in valid:
            return Response({"detail": f"Invalid status. Choose from: {', '.join(sorted(valid))}"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = new_status
        order.save(update_fields=["status", "updated_at"])
        return Response(OrderSerializer(order).data)
