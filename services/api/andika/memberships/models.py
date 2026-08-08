from django.conf import settings
from django.db import models


class MembershipTier(models.Model):
    class Interval(models.TextChoices):
        MONTHLY = "monthly", "Monthly"
        ANNUAL = "annual", "Annual"

    name = models.CharField(max_length=120)
    price_kes = models.DecimalField(max_digits=10, decimal_places=2)
    price_usd = models.DecimalField(max_digits=10, decimal_places=2)
    interval = models.CharField(
        max_length=16, choices=Interval.choices, default=Interval.MONTHLY
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.get_interval_display()})"


class Subscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        PAST_DUE = "past_due", "Past due"
        CANCELED = "canceled", "Canceled"

    class Provider(models.TextChoices):
        MPESA = "mpesa", "M-Pesa"
        PAYPAL = "paypal", "PayPal"

    member = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    tier = models.ForeignKey(
        MembershipTier,
        on_delete=models.PROTECT,
        related_name="subscriptions",
    )
    status = models.CharField(
        max_length=16, choices=Status.choices, default=Status.ACTIVE
    )
    provider = models.CharField(max_length=16, choices=Provider.choices)
    current_period_end = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.member} -> {self.tier} ({self.status})"