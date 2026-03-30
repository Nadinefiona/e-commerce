from rest_framework import serializers

from apps.payments.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "order", "method", "status", "amount", "transaction_id", "paid_at", "created_at"]
        read_only_fields = ["id", "status", "amount", "transaction_id", "paid_at", "created_at"]
