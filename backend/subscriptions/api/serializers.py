from rest_framework import serializers
from subscriptions.models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plan
        fields = ['id', 'name', 'plan_type', 'price_monthly', 'price_yearly', 'ai_credits_monthly', 'features', 'is_active']
        read_only_fields = ['id']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = PlanSerializer(read_only=True)

    class Meta:
        model = Subscription
        fields = ['id', 'plan', 'status', 'current_period_start', 'current_period_end', 'cancel_at_period_end', 'ai_credits_remaining', 'created_at']
        read_only_fields = ['id', 'created_at']
