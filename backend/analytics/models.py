from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class CareerInsight(models.Model):
    class InsightCategory(models.TextChoices):
        SKILL_GAP = 'SKILL_GAP', 'Skill Gap'
        MARKET_TREND = 'MARKET_TREND', 'Market Trend'
        PROFILE_STRENGTH = 'PROFILE_STRENGTH', 'Profile Strength'
        CONTENT_SUGGESTION = 'CONTENT_SUGGESTION', 'Content Suggestion'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='career_insights')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='career_insights')
    category = models.CharField(max_length=32, choices=InsightCategory.choices)
    title = models.CharField(max_length=255)
    description = models.TextField()
    actionable_step = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'analytics_career_insights'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.category}: {self.title}"
