from rest_framework import serializers
from jobs.models import Job, JobSkill, JobSource, JobAnalysis


class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSkill
        fields = ['id', 'name', 'required', 'importance']
        read_only_fields = ['id']


class JobSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSource
        fields = ['id', 'name', 'provider', 'base_url', 'is_active']
        read_only_fields = ['id']


class JobAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAnalysis
        fields = [
            'id', 'match_score', 'matched_skills', 'missing_skills',
            'experience_compatibility', 'career_alignment',
            'potential_concerns', 'recommendation', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class JobSerializer(serializers.ModelSerializer):
    skills = JobSkillSerializer(many=True, read_only=True)
    source = JobSourceSerializer(read_only=True)
    latest_analysis = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'description', 'location', 'work_mode',
            'employment_type', 'salary_min', 'salary_max', 'currency',
            'application_url', 'published_at', 'skills', 'source', 'latest_analysis',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_latest_analysis(self, obj):
        analysis = obj.analyses.first()
        if analysis:
            return JobAnalysisSerializer(analysis).data
        return None
