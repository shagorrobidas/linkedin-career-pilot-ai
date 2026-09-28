from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class UserProfile(models.Model):
    class WorkPreference(models.TextChoices):
        REMOTE = 'REMOTE', 'Remote'
        HYBRID = 'HYBRID', 'Hybrid'
        ON_SITE = 'ON_SITE', 'On-site'
        ANY = 'ANY', 'Any'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='profiles')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    headline = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    career_focus = models.CharField(max_length=255, blank=True)
    years_of_experience = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=255, blank=True)
    remote_preference = models.CharField(
        max_length=32,
        choices=WorkPreference.choices,
        default=WorkPreference.REMOTE
    )
    desired_salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    desired_salary_currency = models.CharField(max_length=10, default='USD')
    resume_url = models.URLField(blank=True)
    profile_completion = models.PositiveIntegerField(default=0)  # 0 - 100 percentage
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'
        unique_together = ('tenant', 'user')

    def __str__(self):
        return f"{self.user.email} Profile"


class Skill(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(default=1)
    is_primary = models.BooleanField(default=False)

    class Meta:
        db_table = 'profile_skills'
        unique_together = ('profile', 'name')

    def __str__(self):
        return f"{self.name} ({self.profile.user.email})"


class WorkExperience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    skills_used = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'profile_experiences'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.title} at {self.company}"


class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_of_study = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = 'profile_educations'

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class ProfileSnapshot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='profile_snapshots')
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='snapshots')
    overall_health_score = models.PositiveIntegerField(default=0)
    headline_score = models.PositiveIntegerField(default=0)
    about_score = models.PositiveIntegerField(default=0)
    skills_score = models.PositiveIntegerField(default=0)
    projects_score = models.PositiveIntegerField(default=0)
    github_score = models.PositiveIntegerField(default=0)
    suggestions = models.JSONField(default=list, blank=True)
    snapshot_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'profile_snapshots'
        ordering = ['-created_at']

    def __str__(self):
        return f"Snapshot {self.created_at.strftime('%Y-%m-%d')} - {self.overall_health_score}%"
