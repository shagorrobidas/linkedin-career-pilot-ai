from django.db import models
from tenants.models import Tenant
import uuid


class JobSource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    provider = models.CharField(max_length=100)
    base_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'job_sources'

    def __str__(self):
        return self.name


class Job(models.Model):
    class WorkMode(models.TextChoices):
        REMOTE = 'REMOTE', 'Remote'
        HYBRID = 'HYBRID', 'Hybrid'
        ON_SITE = 'ON_SITE', 'On-site'

    class EmploymentType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full-time'
        PART_TIME = 'PART_TIME', 'Part-time'
        CONTRACT = 'CONTRACT', 'Contract'
        INTERNSHIP = 'INTERNSHIP', 'Internship'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='jobs')
    source = models.ForeignKey(JobSource, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobs')
    external_id = models.CharField(max_length=255, blank=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    company = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, db_index=True)
    work_mode = models.CharField(max_length=32, choices=WorkMode.choices, default=WorkMode.REMOTE)
    employment_type = models.CharField(max_length=32, choices=EmploymentType.choices, default=EmploymentType.FULL_TIME)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default='USD')
    application_url = models.URLField(max_length=1000, blank=True)
    fingerprint = models.CharField(max_length=64, blank=True, db_index=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jobs'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return f"{self.title} at {self.company}"


class JobSkill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    required = models.BooleanField(default=True)
    importance = models.IntegerField(default=1)  # 1 to 5 scale

    class Meta:
        db_table = 'job_skills'
        unique_together = ('job', 'name')

    def __str__(self):
        return f"{self.name} ({self.job.title})"


class JobAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='job_analyses')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='analyses')
    match_score = models.PositiveIntegerField(default=0)  # 0 to 100
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    experience_compatibility = models.CharField(max_length=255, blank=True)
    career_alignment = models.CharField(max_length=255, blank=True)
    potential_concerns = models.JSONField(default=list, blank=True)
    recommendation = models.CharField(max_length=50, default='MEDIUM_PRIORITY')
    raw_ai_analysis = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'job_analyses'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.job.title} Analysis - {self.match_score}%"
