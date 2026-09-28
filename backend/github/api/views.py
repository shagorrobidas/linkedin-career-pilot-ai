from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from github.models import GitHubRepository
from github.api.serializers import GitHubRepositorySerializer


class GitHubViewSet(viewsets.ModelViewSet):
    queryset = GitHubRepository.objects.all()
    serializer_class = GitHubRepositorySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'GitHub repositories retrieved.',
            'data': serializer.data
        })

    @action(detail=False, methods=['post'])
    def sync(self, request):
        # Trigger background or mock sync
        return Response({
            'success': True,
            'message': 'GitHub sync started. Repositories and recent commits are updating.'
        })
