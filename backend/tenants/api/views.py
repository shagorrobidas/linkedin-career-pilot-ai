from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from tenants.models import Tenant, TenantMember
from tenants.api.serializers import TenantSerializer, TenantMemberSerializer


class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Tenants retrieved successfully.',
            'data': serializer.data
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            tenant = serializer.save(owner=request.user if request.user.is_authenticated else None)
            return Response({
                'success': True,
                'message': 'Tenant created successfully.',
                'data': self.get_serializer(tenant).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'message': 'Invalid tenant data.',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        tenant = self.get_object()
        members = tenant.memberships.all()
        serializer = TenantMemberSerializer(members, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })
