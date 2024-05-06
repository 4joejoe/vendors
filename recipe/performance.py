from .models import STATUS_CHOICES
from django.utils import timezone
from django.db.models import F
from django.apps import apps


class Performance:
    def __init__(self) -> None:
        self.now = timezone.now()

    def on_po_completion(self, instance):
        # On-Time Delivery Rate:
        # ● Calculated each time a PO status changes to 'completed'.
        # ● Logic: Count the number of completed POs delivered on or before
        # delivery_date and divide by the total number of completed POs for that vendor.
        PurchaseOrder = apps.get_model("recipe", "PurchaseOrder")
        Vendor = apps.get_model("recipe", "Vendor")
        completed_orders = PurchaseOrder.objects.filter(status=STATUS_CHOICES.COMPLETED)
        total_completed_orders = completed_orders.count()
        vendor = Vendor.objects.get(id=instance.vendor_reference.id)
        if total_completed_orders > 0:
            on_time_completed_orders = completed_orders.filter(
                actual_delivery_date__lte=F("delivery_date")
            )
            total_on_time_completed_orders = on_time_completed_orders.count()
            on_time_completion_rate = (
                total_on_time_completed_orders / total_completed_orders
            ) * 100
            vendor.on_time_delivery_rate = on_time_completion_rate

        else:
            on_time_completion_rate = None  # or some default value

        # Quality Rating Average:
        # ● Updated upon the completion of each PO where a quality_rating is provided.
        # ● Logic: Calculate the average of all quality_rating values for completed POs of
        # the vendor.

        if instance.quality_rating is not None:
            quality_ratings = completed_orders.filter(
                quality_rating__isnull=False
            ).values_list("quality_rating", flat=True)
            average_quality_rating = (
                sum(quality_ratings) / len(quality_ratings) if quality_ratings else None
            )
            vendor.quality_rating_avg = average_quality_rating

        vendor.save()

    # Average Response Time:
    # ● Calculated each time a PO is acknowledged by the vendor.
    # ● Logic: Compute the time difference between issue_date and
    # acknowledgment_date for each PO, and then find the average of these times
    # for all POs of the vendor.

    def on_po_acknowledgement(self, instance):
        PurchaseOrder = apps.get_model("recipe", "PurchaseOrder")

        Vendor = apps.get_model("recipe", "Vendor")
        vendor = Vendor.objects.get(id=instance.vendor_reference.id)
        # Get all acknowledged POs for this vendor

        acknowledged_pos = PurchaseOrder.objects.filter(
            vendor_reference=vendor, acknowledgement_date__isnull=False
        )

        # Calculate response time for each PO and find the average
        total_response_time = 0
        for po in acknowledged_pos:
            response_time = (
                po.acknowledgement_date - po.issue_date
            ).total_seconds() / 86400
            total_response_time += response_time

        vendor.average_response_time = (
            total_response_time / len(acknowledged_pos) if acknowledged_pos else None
        )
        vendor.save()

    # Fulfillment Rate:
    # ● Calculated upon any change in PO status.
    # ● Logic: Divide the number of successfully fulfilled POs (status 'completed'
    # without issues) by the total number of POs issued to the vendor.

    def fulfillment_rate(self, instance):
        PurchaseOrder = apps.get_model("recipe", "PurchaseOrder")
        Vendor = apps.get_model("recipe", "Vendor")
        vendor = Vendor.objects.get(id=instance.vendor_reference.id)
        total_orders = PurchaseOrder.objects.filter(vendor_reference=vendor).count()
        completed_orders = PurchaseOrder.objects.filter(
            vendor_reference=vendor, status=STATUS_CHOICES.COMPLETED
        ).count()
        fulfillment_rate = (
            (completed_orders / total_orders) * 100 if total_orders > 0 else 0
        )
        vendor.fulfillment_rate = fulfillment_rate
        vendor.save()
