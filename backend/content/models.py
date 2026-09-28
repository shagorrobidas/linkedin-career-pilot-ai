from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class PostTopic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='Technical')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'content_topics'

    def __str__(self):
        return self.name


class LinkedInPost(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', 'Draft'
        REVIEW = 'REVIEW', 'Review'
        APPROVED = 'APPROVED', 'Approved'
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        PUBLISHED = 'PUBLISHED', 'Published'
        ARCHIVED = 'ARCHIVED', 'Archived'

    class Tone(models.TextChoices):
        PROFESSIONAL = 'PROFESSIONAL', 'Professional'
        CASUAL = 'CASUAL', 'Casual'
        THOUGHT_LEADERSHIP = 'THOUGHT_LEADERSHIP', 'Thought Leadership'
        STORYTELLING = 'STORYTELLING', 'Storytelling'
        EDUCATIONAL = 'EDUCATIONAL', 'Educational'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    topic = models.CharField(max_length=255)
    content = models.TextField()
    tone = models.CharField(max_length=32, choices=Tone.choices, default=Tone.PROFESSIONAL)
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.DRAFT, db_index=True)
    scheduled_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    ai_generated = models.BooleanField(default=True)
    human_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'linkedin_posts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.topic} ({self.status})"


class PostPerformance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.OneToOneField(LinkedInPost, on_delete=models.CASCADE, related_name='performance')
    impressions = models.PositiveIntegerField(default=0)
    reactions = models.PositiveIntegerField(default=0)
    comments = models.PositiveIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)
    profile_views_generated = models.PositiveIntegerField(default=0)
    recorded_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'post_performances'

    def __str__(self):
        return f"Performance for {self.post.topic}: {self.impressions} impressions"
