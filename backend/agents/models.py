from django.db import models
from django.conf import settings
from tenants.models import Tenant
import uuid


class Agent(models.Model):
    class Provider(models.TextChoices):
        OPENAI = 'OPENAI', 'OpenAI'
        GEMINI = 'GEMINI', 'Google Gemini'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    provider = models.CharField(max_length=32, choices=Provider.choices, default=Provider.GEMINI)
    model_name = models.CharField(max_length=100, default='gemini-1.5-pro')
    system_prompt = models.TextField(blank=True)
    credit_cost = models.PositiveIntegerField(default=2)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'agents'
        ordering = ['name']

    def __str__(self):
        return self.name


class AgentTask(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        QUEUED = 'QUEUED', 'Queued'
        RUNNING = 'RUNNING', 'Running'
        COMPLETED = 'COMPLETED', 'Completed'
        FAILED = 'FAILED', 'Failed'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='agent_tasks')
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='tasks')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='agent_tasks')
    status = models.CharField(max_length=32, choices=Status.choices, default=Status.PENDING)
    input_payload = models.JSONField(default=dict)
    output_payload = models.JSONField(default=dict, blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'agent_tasks'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agent.name} Task ({self.status})"


class AgentExecution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.OneToOneField(AgentTask, on_delete=models.CASCADE, related_name='execution')
    duration_ms = models.PositiveIntegerField(default=0)
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    credits_consumed = models.PositiveIntegerField(default=0)
    provider_response_id = models.CharField(max_length=255, blank=True)
    executed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'agent_executions'

    def __str__(self):
        return f"Execution of {self.task.agent.name} - {self.credits_consumed} credits"


class AIUsage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='ai_usages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ai_usages')
    agent_name = models.CharField(max_length=100)
    provider = models.CharField(max_length=32)
    model = models.CharField(max_length=100)
    prompt_version = models.CharField(max_length=32, default='v1.0')
    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    credits_used = models.PositiveIntegerField(default=1)
    latency_ms = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=32, default='SUCCESS')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_usages'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.agent_name} - {self.credits_used} credits"


class AICreditTransaction(models.Model):
    class TransactionType(models.TextChoices):
        PURCHASE = 'PURCHASE', 'Purchase'
        PLAN_GRANT = 'PLAN_GRANT', 'Plan Grant'
        CONSUMPTION = 'CONSUMPTION', 'Consumption'
        REFUND = 'REFUND', 'Refund'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='credit_transactions')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='credit_transactions')
    transaction_type = models.CharField(max_length=32, choices=TransactionType.choices)
    amount = models.IntegerField()  # positive for grants, negative for consumption
    balance_after = models.PositiveIntegerField()
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ai_credit_transactions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.transaction_type}: {self.amount} (Balance: {self.balance_after})"
