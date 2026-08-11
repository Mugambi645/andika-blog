from django.db import models

# Create your models here.
from andika.memberships.models import Subscription

class Payment(models.Model):
    class Provider(models.TextChoices):
        MPESA = "mpesa", "M-Pesa"
        PAYPAL = "paypal", "PayPal"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"

    provider = models.CharField(max_length=16, choices=Provider.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=8, default="KES")
    status = models.CharField(
        max_length=16, choices=Status.choices, default=
        Status.PENDING
    )
    checkout_request_id = models.CharField(max_length=64, blank=True, db_index=True)
    paypal_order_id = models.CharField(
        max_length=64, blank=True, db_index=True
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.provider} {self.amount} {self.currency} ({self.status})"

    