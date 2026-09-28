from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from jobs.models import Job, JobAnalysis
from jobs.api.serializers import JobSerializer, JobAnalysisSerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

    def list(self, request, *args, **kwargs):
        work_mode = request.query_params.get('work_mode')
        search = request.query_params.get('search')
        queryset = self.get_queryset()
        if work_mode:
            queryset = queryset.filter(work_mode=work_mode)
        if search:
            queryset = queryset.filter(title__icontains=search)

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'success': True,
            'message': 'Jobs retrieved successfully.',
            'count': queryset.count(),
            'data': serializer.data
        })

    @action(detail=True, methods=['post'])
    def analyze(self, request, pk=None):
        job = self.get_object()
        # Mock / invoke AI Job Analyzer
        analysis, _ = JobAnalysis.objects.get_or_create(
            job=job,
            tenant=job.tenant,
            defaults={
                'match_score': 94,
                'matched_skills': ['Python', 'Django', 'PostgreSQL', 'Redis'],
                'missing_skills': ['Kubernetes'],
                'experience_compatibility': 'High match with 3+ years backend experience',
                'career_alignment': 'Strong alignment with Senior Backend Developer goal',
                'recommendation': 'HIGH_PRIORITY'
            }
        )
        return Response({
            'success': True,
            'message': 'Job analyzed successfully.',
            'data': JobAnalysisSerializer(analysis).data
        })

    @action(detail=True, methods=['post'])
    def save_job(self, request, pk=None):
        job = self.get_object()
        return Response({
            'success': True,
            'message': f"Job '{job.title}' saved to your tracker."
        })
