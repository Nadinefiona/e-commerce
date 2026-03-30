import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.notifications.models import Notification
from apps.orders.models import Order

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def notify_order_status(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.user,
            message=f"Your order #{instance.id} has been placed successfully.",
        )
        logger.info("Notification sent for new order #%s", instance.id)
    else:
        Notification.objects.create(
            user=instance.user,
            message=f"Your order #{instance.id} status changed to {instance.get_status_display()}.",
        )
