from django.urls import path, include
from rest_framework.routers import DefaultRouter
from github.api.views import GitHubViewSet

router = DefaultRouter()
router.register(r'repositories', GitHubViewSet, basename='github-repo')

urlpatterns = [
    path('', include(router.urls)),
]
