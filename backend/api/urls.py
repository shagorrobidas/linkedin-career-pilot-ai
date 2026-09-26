
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.api.urls')),
    path('agents/', include('agents.api.urls')),
    path('analytics/', include('analytics.api.urls')),
    path('applications/', include('applications.api.urls')),
    path('billing/', include('billing.api.urls')),
    path('content/', include('content.api.urls')),
    path('github/', include('github.api.urls')),
    path('jobs/', include('jobs.api.urls')),
    path('notifications/', include('notifications.api.urls')),
    path('profiles/', include('profiles.api.urls')),
    path('subscriptions/', include('subscriptions.api.urls')),
    path('tenants/', include('tenants.api.urls')),
    
]