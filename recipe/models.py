import random
import string
from collections import namedtuple
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from django.conf import settings

Status = namedtuple("Status", ["DRAFT", "PENDING", "COMPLETED", "CANCELLED"])
STATUS_CHOICES = Status("draft", "pending", "completed", "cancelled")
STATUS_CHOICES_FOR_FIELD = [(field, field) for field in STATUS_CHOICES]


def generate_unique_code():
    length = 6
    while True:
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if Vendor.objects.filter(vendor_code=code).count() == 0:
            break
    return code


class Vendor(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vendors",
    )
    vendor_code = models.CharField(
        max_length=7, default=generate_unique_code, unique=True, editable=False
    )
    name = models.CharField(max_length=200)
    contact_details = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    on_time_delivery_rate = models.FloatField(
        verbose_name=_("On Time Delivery Rate"), null=True
    )
    quality_rating_avg = models.FloatField(
        verbose_name=_("Quality Rating Average"), null=True
    )
    average_response_time = models.FloatField(
        verbose_name=("Average Response Time"), null=True
    )
    fulfillment_rate = models.FloatField(verbose_name=("Fulfillment Rate"), null=True)


class PurchaseOrder(models.Model):
    po_number = models.CharField(
        max_length=7, default=generate_unique_code, unique=True, editable=False
    )
    vendor_reference = models.ForeignKey(
        Vendor, on_delete=models.PROTECT, verbose_name="Vendor"
    )
    items = models.JSONField()
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES_FOR_FIELD, default=STATUS_CHOICES.DRAFT
    )
    quality_rating = models.FloatField(_(""), default=None, null=True)

    order_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True, null=True)
    acknowledgement_date = models.DateTimeField(null=True)
    actual_delivery_date = models.DateTimeField(null=True)


class PerformanceMetrics(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.PROTECT, verbose_name="Vendor")
    date = models.DateTimeField(auto_now_add=True, null=True)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)
