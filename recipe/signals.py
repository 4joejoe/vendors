from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from recipe.models import STATUS_CHOICES, PerformanceMetrics, PurchaseOrder, Vendor
from recipe.performance import Performance


@receiver(post_save, sender=Vendor)
def create_performance_metrics(sender, instance, created, **kwargs):
    if created:
        PerformanceMetrics.objects.create(vendor=instance)


@receiver(post_save, sender=PurchaseOrder)
def is_po_completed(sender, instance, **kwargs):
    if instance.status == STATUS_CHOICES.COMPLETED:
        print("-->Django Signals<--", instance.status)
        performance = Performance()
        performance.on_po_completion(instance=instance)
    return False


@receiver(post_save, sender=Vendor)
def update_performance_metrics(sender, instance, **kwargs):
    # update fields of PerformanceMetrics model

    performance_metrics = PerformanceMetrics.objects.get(vendor=instance)
    performance_metrics.on_time_delivery_rate = instance.on_time_delivery_rate
    performance_metrics.quality_rating_avg = instance.quality_rating_avg
    performance_metrics.average_response_time = instance.average_response_time
    performance_metrics.fulfillment_rate = instance.fulfillment_rate
    performance_metrics.save()


@receiver(pre_save, sender=PurchaseOrder)
def average_response_time(sender, instance, **kwargs):
    # Calculated each time a PO is acknowledged by the vendor.
    # ● Logic: Compute the time difference between issue_date and
    # acknowledgment_date for each PO, and then find the average of these times
    # for all POs of the vendor.
    # get previous value from db and new values of acknowledgment_date from request and if it is changed then calculate average response time using pre_save signal

    print(instance.acknowledgement_date)
    if instance.acknowledgement_date:
        performance = Performance()
        performance.on_po_acknowledgement(instance=instance)

    # Fulfillment Rate:
    # ● Calculated upon any change in PO status.
    # ● Logic: Divide the number of successfully fulfilled POs (status 'completed'
    # without issues) by the total number of POs issued to the vendor.


@receiver(post_save, sender=PurchaseOrder)
def on_po_status_change(sender, instance, **kwargs):
    if instance.status:
        performance = Performance()
        performance.fulfillment_rate(instance=instance)
    return False
