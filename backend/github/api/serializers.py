from rest_framework import serializers
from github.models import GitHubRepository, GitHubActivity, GitHubInsight


class GitHubActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubActivity
        fields = ['id', 'activity_type', 'title', 'description', 'technologies_detected', 'occurred_at']
        read_only_fields = ['id']


class GitHubInsightSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubInsight
        fields = ['id', 'insight_text', 'suggested_post_topic', 'created_at']
        read_only_fields = ['id', 'created_at']


class GitHubRepositorySerializer(serializers.ModelSerializer):
    activities = GitHubActivitySerializer(many=True, read_only=True)
    insights = GitHubInsightSerializer(many=True, read_only=True)

    class Meta:
        model = GitHubRepository
        fields = [
            'id', 'repo_name', 'full_name', 'description', 'html_url',
            'primary_language', 'languages', 'stars_count', 'forks_count',
            'is_fork', 'is_private', 'activities', 'insights', 'last_synced_at'
        ]
        read_only_fields = ['id', 'last_synced_at']
