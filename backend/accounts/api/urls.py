from django.urls import path
from accounts.api.views import RegisterView, LoginView, UserProfileMeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth-register'),
    path('login/', LoginView.as_view(), name='auth-login'),
    path('me/', UserProfileMeView.as_view(), name='auth-me'),
]
