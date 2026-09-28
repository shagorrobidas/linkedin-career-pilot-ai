from rest_framework import serializers
from applications.models import JobApplication, Interview
from jobs.api.serializers import JobSerializer


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'stage', 'scheduled_at', 'interviewer_info', 'meeting_link', 'notes', 'feedback']
        read_only_fields = ['id']


class JobApplicationSerializer(serializers.ModelSerializer):
    job_details = JobSerializer(source='job', read_only=True)
    interviews = InterviewSerializer(many=True, read_only=True)

    class Meta:
        model = JobApplication
        fields = [
            'id', 'job', 'job_details', 'status', 'resume_version',
            'cover_letter', 'recruiter_name', 'recruiter_email',
            'applied_date', 'follow_up_date', 'notes', 'interviews',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
