from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class GitHubRepository(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='github_repositories')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='github_repositories')
    repo_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    html_url = models.URLField()
    primary_language = models.CharField(max_length=100, blank=True)
    languages = models.JSONField(default=dict, blank=True)
    stars_count = models.PositiveIntegerField(default=0)
    forks_count = models.PositiveIntegerField(default=0)
    is_fork = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    last_synced_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'github_repositories'
        unique_together = ('tenant', 'full_name')

    def __str__(self):
        return self.full_name


class GitHubActivity(models.Model):
    class ActivityType(models.TextChoices):
        COMMIT = 'COMMIT', 'Commit'
        RELEASE = 'RELEASE', 'Release'
        PULL_REQUEST = 'PULL_REQUEST', 'Pull Request'
        ISSUE = 'ISSUE', 'Issue'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=32, choices=ActivityType.choices)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    technologies_detected = models.JSONField(default=list, blank=True)
    occurred_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'github_activities'
        ordering = ['-occurred_at']

    def __str__(self):
        return f"{self.activity_type}: {self.title}"


class GitHubInsight(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='github_insights')
    repository = models.ForeignKey(GitHubRepository, on_delete=models.CASCADE, related_name='insights')
    insight_text = models.TextField()
    suggested_post_topic = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'github_insights'

    def __str__(self):
        return f"Insight for {self.repository.repo_name}"
