from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from agents.models import Agent, AgentTask, AgentExecution, AIUsage, AICreditTransaction
from agents.api.serializers import AgentSerializer, AgentTaskSerializer, AIUsageSerializer, AICreditTransactionSerializer
from tenants.models import Tenant


class AgentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer

    @action(detail=True, methods=['post'])
    def run(self, request, pk=None):
        agent = self.get_object()
        tenant = Tenant.objects.first()
        user = request.user if request.user.is_authenticated else (tenant.owner if tenant else None)

        task = AgentTask.objects.create(
            tenant=tenant,
            agent=agent,
            user=user,
            status=AgentTask.Status.COMPLETED,
            input_payload=request.data,
            output_payload={"result": f"Execution completed by {agent.name}"}
        )
        AgentExecution.objects.create(
            task=task,
            duration_ms=450,
            input_tokens=120,
            output_tokens=340,
            credits_consumed=agent.credit_cost
        )
        return Response({
            'success': True,
            'message': f"Task initiated and executed for {agent.name}.",
            'data': AgentTaskSerializer(task).data
        })


class AgentTaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AgentTask.objects.all()
    serializer_class = AgentTaskSerializer


class AICreditsView(APIView):
    def get(self, request):
        return Response({
            'success': True,
            'data': {
                'credits_available': 82,
                'credits_total': 100,
                'used_this_month': 18
            }
        })
