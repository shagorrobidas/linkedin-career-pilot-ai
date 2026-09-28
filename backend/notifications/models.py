from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class Notification(models.Model):
    class NotificationType(models.TextChoices):
        HIGH_MATCH_JOB = 'HIGH_MATCH_JOB', 'High Match Job'
        AI_CONTENT_DRAFT = 'AI_CONTENT_DRAFT', 'AI Content Draft Ready'
        APPLICATION_REMINDER = 'APPLICATION_REMINDER', 'Application Reminder'
        INTERVIEW_REMINDER = 'INTERVIEW_REMINDER', 'Interview Reminder'
        PROFILE_HEALTH = 'PROFILE_HEALTH', 'Profile Health Alert'
        CREDIT_LOW = 'CREDIT_LOW', 'Low AI Credits'
        SUBSCRIPTION = 'SUBSCRIPTION', 'Subscription Update'
        GITHUB_ACTIVITY = 'GITHUB_ACTIVITY', 'GitHub Activity Sync'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='notifications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=64, choices=NotificationType.choices)
    title = models.CharField(max_length=255)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.email} - {self.title}"


class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notification_preference')
    email_enabled = models.BooleanField(default=True)
    telegram_enabled = models.BooleanField(default=False)
    telegram_chat_id = models.CharField(max_length=100, blank=True)
    high_match_jobs_notify = models.BooleanField(default=True)
    content_drafts_notify = models.BooleanField(default=True)
    interview_reminders_notify = models.BooleanField(default=True)

    class Meta:
        db_table = 'notification_preferences'

    def __str__(self):
        return f"Preferences for {self.user.email}"
