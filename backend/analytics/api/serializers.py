from rest_framework import serializers
from analytics.models import CareerInsight


class CareerInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerInsight
        fields = ['id', 'category', 'title', 'description', 'actionable_step', 'created_at']
        read_only_fields = ['id', 'created_at']
