from django.urls import path

from apps.payments.views import CreatePaymentAPIView

urlpatterns = [
    path("pay/", CreatePaymentAPIView.as_view(), name="create-payment"),
]
