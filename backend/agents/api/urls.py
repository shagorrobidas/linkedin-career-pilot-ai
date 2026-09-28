from django.urls import path, include
from rest_framework.routers import DefaultRouter
from agents.api.views import AgentViewSet, AgentTaskViewSet, AICreditsView

router = DefaultRouter()
router.register(r'tasks', AgentTaskViewSet, basename='agent-task')
router.register(r'', AgentViewSet, basename='agent')

urlpatterns = [
    path('credits/', AICreditsView.as_view(), name='ai-credits'),
    path('', include(router.urls)),
]
