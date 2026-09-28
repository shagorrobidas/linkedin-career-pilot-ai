from django.urls import path
from profiles.api.views import ProfileDetailView, ProfileHealthView

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='profile-me'),
    path('health/', ProfileHealthView.as_view(), name='profile-health'),
]
