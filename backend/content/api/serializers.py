from rest_framework import serializers
from content.models import LinkedInPost, PostTopic, PostPerformance


class PostTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostTopic
        fields = ['id', 'name', 'category', 'is_active']
        read_only_fields = ['id']


class PostPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostPerformance
        fields = ['id', 'impressions', 'reactions', 'comments', 'shares', 'profile_views_generated', 'recorded_at']
        read_only_fields = ['id', 'recorded_at']


class LinkedInPostSerializer(serializers.ModelSerializer):
    performance = PostPerformanceSerializer(read_only=True)

    class Meta:
        model = LinkedInPost
        fields = [
            'id', 'topic', 'content', 'tone', 'status', 'scheduled_at',
            'published_at', 'ai_generated', 'human_approved', 'performance',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
