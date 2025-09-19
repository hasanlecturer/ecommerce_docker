from django.db.models.signals import pre_save
from .models import Order
from django.dispatch import receiver

@receiver(pre_save, sender=Order)
def generate_order_number(sender, instance, **kwargs):
    """
    Signal to generate a unique order number before saving an Order instance.
    The order number is generated only if it is not already set.
    """
    if not instance.order_number:
        last_order = Order.objects.all().order_by("-id").first()
        if last_order and last_order.order_number: #ord-001
            try:
                last_order_number = int(last_order.order_number.split("-")[-1])
            except ValueError:
                last_order_number = 0
            new_order_number = last_order_number + 1
        else:
            new_order_number = 1
            
        instance.order_number = f"ord-{new_order_number:04d}" # ord-0001, ord-0002, ord-0003, ...
