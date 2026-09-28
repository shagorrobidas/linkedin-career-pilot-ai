from django.db import models
from django.conf import settings
from tenants.models import Tenant
from jobs.models import Job
import uuid


class JobApplication(models.Model):
    class Status(models.TextChoices):
        NEW = 'NEW', 'New'
        REVIEWED = 'REVIEWED', 'Reviewed'
        SAVED = 'SAVED', 'Saved'
        APPLIED = 'APPLIED', 'Applied'
        INTERVIEW = 'INTERVIEW', 'Interview'
        OFFER = 'OFFER', 'Offer'
        REJECTED = 'REJECTED', 'Rejected'
        ARCHIVED = 'ARCHIVED', 'Archived'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.SAVED, db_index=True)
    resume_version = models.CharField(max_length=255, blank=True)
    cover_letter = models.TextField(blank=True)
    recruiter_name = models.CharField(max_length=255, blank=True)
    recruiter_email = models.EmailField(blank=True)
    applied_date = models.DateField(null=True, blank=True)
    follow_up_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'job_applications'
        unique_together = ('tenant', 'user', 'job')
        ordering = ['-updated_at']

    def __str__(self):
        return f"{self.job.title} ({self.status})"


class Interview(models.Model):
    class Stage(models.TextChoices):
        SCREENING = 'SCREENING', 'Recruiter Screening'
        TECHNICAL = 'TECHNICAL', 'Technical Interview'
        SYSTEM_DESIGN = 'SYSTEM_DESIGN', 'System Design'
        BEHAVIORAL = 'BEHAVIORAL', 'Behavioral / Culture Fit'
        FINAL = 'FINAL', 'Final Round / Executive'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name='interviews')
    stage = models.CharField(max_length=32, choices=Stage.choices, default=Stage.TECHNICAL)
    scheduled_at = models.DateTimeField()
    interviewer_info = models.CharField(max_length=255, blank=True)
    meeting_link = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'application_interviews'
        ordering = ['-scheduled_at']

    def __str__(self):
        return f"{self.application.job.company} - {self.stage}"
