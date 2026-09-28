from rest_framework import serializers
from agents.models import Agent, AgentTask, AgentExecution, AIUsage, AICreditTransaction


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ['id', 'name', 'slug', 'description', 'provider', 'model_name', 'credit_cost', 'is_active']
        read_only_fields = ['id']


class AgentExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgentExecution
        fields = ['id', 'duration_ms', 'input_tokens', 'output_tokens', 'credits_consumed', 'executed_at']
        read_only_fields = ['id', 'executed_at']


class AgentTaskSerializer(serializers.ModelSerializer):
    agent_info = AgentSerializer(source='agent', read_only=True)
    execution = AgentExecutionSerializer(read_only=True)

    class Meta:
        model = AgentTask
        fields = ['id', 'agent', 'agent_info', 'status', 'input_payload', 'output_payload', 'error_message', 'execution', 'created_at']
        read_only_fields = ['id', 'created_at']


class AIUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIUsage
        fields = ['id', 'agent_name', 'provider', 'model', 'prompt_version', 'input_tokens', 'output_tokens', 'credits_used', 'latency_ms', 'status', 'created_at']
        read_only_fields = ['id', 'created_at']


class AICreditTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AICreditTransaction
        fields = ['id', 'transaction_type', 'amount', 'balance_after', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
