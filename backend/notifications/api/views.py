from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from notifications.models import Notification, NotificationPreference
from notifications.api.serializers import NotificationSerializer, NotificationPreferenceSerializer
from django.utils import timezone


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save()
        return Response({
            'success': True,
            'message': 'Notification marked as read.'
        })


class NotificationPreferencesView(APIView):
    def get(self, request):
        pref = NotificationPreference.objects.first()
        if pref:
            return Response({'success': True, 'data': NotificationPreferenceSerializer(pref).data})
        return Response({
            'success': True,
            'data': {
                'email_enabled': True,
                'telegram_enabled': False,
                'high_match_jobs_notify': True,
                'content_drafts_notify': True,
                'interview_reminders_notify': True
            }
        })
