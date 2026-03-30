import uuid

from django.utils import timezone
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.orders.models import Order
from apps.payments.models import Payment
from apps.payments.serializers import PaymentSerializer


class CreatePaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order")
        method = request.data.get("method")

        if not order_id:
            return Response({"detail": "Please provide an order ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found. Please check the order ID."}, status=status.HTTP_404_NOT_FOUND)

        if hasattr(order, "payment"):
            return Response({"detail": "This order has already been paid."}, status=status.HTTP_400_BAD_REQUEST)

        valid_methods = {c[0] for c in Payment.Method.choices}
        if method not in valid_methods:
            return Response(
                {"detail": f"Invalid payment method. Choose from: {', '.join(sorted(valid_methods))}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payment = Payment.objects.create(
            order=order,
            method=method,
            amount=order.total_amount,
            status=Payment.Status.COMPLETED,
            transaction_id=str(uuid.uuid4()),
            paid_at=timezone.now(),
        )

        order.status = Order.Status.CONFIRMED
        order.save(update_fields=["status", "updated_at"])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_201_CREATED)
