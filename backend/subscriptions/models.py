from django.db import models
from tenants.models import Tenant
import uuid


class Plan(models.Model):
    class PlanType(models.TextChoices):
        FREE = 'FREE', 'Free'
        PRO = 'PRO', 'Pro'
        PREMIUM = 'PREMIUM', 'Premium'
        TEAM = 'TEAM', 'Team'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=32, choices=PlanType.choices, unique=True)
    price_monthly = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    price_yearly = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    ai_credits_monthly = models.PositiveIntegerField(default=50)
    features = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'subscription_plans'

    def __str__(self):
        return self.name


class Subscription(models.Model):
    class Status(models.TextChoices):
        TRIALING = 'TRIALING', 'Trialing'
        ACTIVE = 'ACTIVE', 'Active'
        PAST_DUE = 'PAST_DUE', 'Past Due'
        CANCELED = 'CANCELED', 'Canceled'
        EXPIRED = 'EXPIRED', 'Expired'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.OneToOneField(Tenant, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.ACTIVE)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    cancel_at_period_end = models.BooleanField(default=False)
    ai_credits_remaining = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subscriptions'

    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name} ({self.status})"
