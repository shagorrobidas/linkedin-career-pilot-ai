from django.urls import path, include
from rest_framework.routers import DefaultRouter
from notifications.api.views import NotificationViewSet, NotificationPreferencesView

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('preferences/', NotificationPreferencesView.as_view(), name='notification-preferences'),
    path('', include(router.urls)),
]
