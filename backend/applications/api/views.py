from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from applications.models import JobApplication
from applications.api.serializers import JobApplicationSerializer


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer

    def list(self, request, *args, **kwargs):
        status_filter = request.query_params.get('status')
        queryset = self.get_queryset()
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        application = self.get_object()
        new_status = request.data.get('status')
        if new_status in JobApplication.Status.values:
            application.status = new_status
            application.save()
            return Response({
                'success': True,
                'message': f"Application status updated to {new_status}.",
                'data': self.get_serializer(application).data
            })
        return Response({
            'success': False,
            'message': 'Invalid status provided.'
        }, status=status.HTTP_400_BAD_REQUEST)
