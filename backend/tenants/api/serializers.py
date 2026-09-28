from rest_framework import serializers
from tenants.models import Tenant, TenantMember
from accounts.api.serializers import UserSerializer


class TenantMemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TenantMember
        fields = ['id', 'user', 'role', 'is_active', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class TenantSerializer(serializers.ModelSerializer):
    members = TenantMemberSerializer(source='memberships', many=True, read_only=True)

    class Meta:
        model = Tenant
        fields = ['id', 'name', 'slug', 'owner', 'members', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
