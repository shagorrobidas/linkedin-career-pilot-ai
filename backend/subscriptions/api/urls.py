from django.urls import path, include
from rest_framework.routers import DefaultRouter
from subscriptions.api.views import PlanViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'plans', PlanViewSet, basename='plan')
router.register(r'current', SubscriptionViewSet, basename='subscription-current')

urlpatterns = [
    path('', include(router.urls)),
]
