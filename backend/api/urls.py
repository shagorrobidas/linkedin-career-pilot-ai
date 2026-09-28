
from django.urls import path, include

from api.views import DashboardOverviewView

urlpatterns = [
    path('auth/', include('accounts.api.urls')),
    path('accounts/', include('accounts.api.urls')),
    path('tenants/', include('tenants.api.urls')),
    path('profile/', include('profiles.api.urls')),
    path('profiles/', include('profiles.api.urls')),
    path('jobs/', include('jobs.api.urls')),
    path('applications/', include('applications.api.urls')),
    path('content/', include('content.api.urls')),
    path('github/', include('github.api.urls')),
    path('agents/', include('agents.api.urls')),
    path('ai/', include('agents.api.urls')),
    path('subscriptions/', include('subscriptions.api.urls')),
    path('billing/', include('billing.api.urls')),
    path('notifications/', include('notifications.api.urls')),
    path('analytics/', include('analytics.api.urls')),
    path('dashboard/', DashboardOverviewView.as_view(), name='dashboard-overview'),
]