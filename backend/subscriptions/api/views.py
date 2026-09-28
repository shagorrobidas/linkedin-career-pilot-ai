from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from subscriptions.models import Plan, Subscription
from subscriptions.api.serializers import PlanSerializer, SubscriptionSerializer


class PlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Plan.objects.filter(is_active=True)
    serializer_class = PlanSerializer


class SubscriptionViewSet(viewsets.ViewSet):
    def list(self, request):
        sub = Subscription.objects.first()
        if sub:
            return Response({
                'success': True,
                'data': SubscriptionSerializer(sub).data
            })
        return Response({
            'success': True,
            'data': {
                'plan': {'name': 'Free', 'plan_type': 'FREE', 'ai_credits_monthly': 20},
                'status': 'ACTIVE',
                'ai_credits_remaining': 15
            }
        })

    @action(detail=False, methods=['post'])
    def change_plan(self, request):
        plan_type = request.data.get('plan_type', 'PRO')
        return Response({
            'success': True,
            'message': f"Subscription updated to {plan_type} plan."
        })
