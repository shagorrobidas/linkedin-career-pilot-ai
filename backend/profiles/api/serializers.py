from rest_framework import serializers
from profiles.models import UserProfile, Skill, WorkExperience, Education, ProfileSnapshot


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'years_of_experience', 'is_primary']
        read_only_fields = ['id']


class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = ['id', 'title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'description', 'skills_used']
        read_only_fields = ['id']


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = ['id', 'institution', 'degree', 'field_of_study', 'start_date', 'end_date']
        read_only_fields = ['id']


class ProfileSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileSnapshot
        fields = ['id', 'overall_health_score', 'headline_score', 'about_score', 'skills_score', 'projects_score', 'github_score', 'suggestions', 'created_at']
        read_only_fields = ['id', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)
    experiences = WorkExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'id', 'headline', 'about', 'career_focus', 'years_of_experience',
            'location', 'remote_preference', 'desired_salary_min', 'desired_salary_currency',
            'resume_url', 'profile_completion', 'skills', 'experiences', 'educations',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
