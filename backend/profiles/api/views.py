from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from profiles.models import UserProfile, ProfileSnapshot
from profiles.api.serializers import UserProfileSerializer, ProfileSnapshotSerializer


class ProfileDetailView(APIView):
    def get(self, request):
        profile = UserProfile.objects.first()
        if not profile:
            return Response({
                'success': True,
                'message': 'No profile found, please initialize profile.',
                'data': None
            })
        serializer = UserProfileSerializer(profile)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def patch(self, request):
        profile = UserProfile.objects.first()
        if not profile:
            return Response({'success': False, 'message': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Profile updated successfully.',
                'data': serializer.data
            })
        return Response({'success': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ProfileHealthView(APIView):
    def get(self, request):
        snapshot = ProfileSnapshot.objects.first()
        health_data = {
            'overall_health_score': snapshot.overall_health_score if snapshot else 87,
            'headline_score': snapshot.headline_score if snapshot else 92,
            'about_score': snapshot.about_score if snapshot else 76,
            'skills_score': snapshot.skills_score if snapshot else 94,
            'projects_score': snapshot.projects_score if snapshot else 90,
            'github_score': snapshot.github_score if snapshot else 88,
            'suggestions': snapshot.suggestions if snapshot else [
                'Add recent backend architecture experience to your About section.',
                'Add Docker and Celery to top highlighted skills.'
            ]
        }
        return Response({
            'success': True,
            'data': health_data
        })
