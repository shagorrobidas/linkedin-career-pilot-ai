from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from content.models import LinkedInPost, PostTopic
from content.api.serializers import LinkedInPostSerializer, PostTopicSerializer
from tenants.models import Tenant


class ContentViewSet(viewsets.ModelViewSet):
    queryset = LinkedInPost.objects.all()
    serializer_class = LinkedInPostSerializer

    @action(detail=False, methods=['post'])
    def generate(self, request):
        topic = request.data.get('topic', 'Django Performance Tuning')
        tone = request.data.get('tone', 'PROFESSIONAL')
        tenant = Tenant.objects.first()
        user = request.user if request.user.is_authenticated else (tenant.owner if tenant else None)

        generated_content = (
            f"🚀 Key learnings on {topic}:\n\n"
            "Optimizing Django query performance starts with understanding ORM evaluation. "
            "Using select_related for foreign keys and prefetch_related for M2M cut database queries by 85% in production.\n\n"
            "#Django #Python #BackendEngineering #Performance"
        )

        post = None
        if tenant and user:
            post = LinkedInPost.objects.create(
                tenant=tenant,
                author=user,
                topic=topic,
                content=generated_content,
                tone=tone,
                status=LinkedInPost.Status.DRAFT,
                ai_generated=True
            )
            return Response({
                'success': True,
                'message': 'AI Post Draft generated successfully.',
                'data': self.get_serializer(post).data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': True,
            'message': 'Post generated preview.',
            'data': {
                'topic': topic,
                'content': generated_content,
                'tone': tone,
                'status': 'DRAFT'
            }
        })

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        post = self.get_object()
        post.human_approved = True
        post.status = LinkedInPost.Status.APPROVED
        post.save()
        return Response({
            'success': True,
            'message': 'Post approved for publishing.',
            'data': self.get_serializer(post).data
        })

    @action(detail=True, methods=['post'])
    def schedule(self, request, pk=None):
        post = self.get_object()
        scheduled_at = request.data.get('scheduled_at')
        post.scheduled_at = scheduled_at
        post.status = LinkedInPost.Status.SCHEDULED
        post.save()
        return Response({
            'success': True,
            'message': f"Post scheduled for {scheduled_at}.",
            'data': self.get_serializer(post).data
        })
