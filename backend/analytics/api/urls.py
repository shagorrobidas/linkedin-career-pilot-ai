from django.urls import path
from analytics.api.views import AnalyticsSummaryView, CareerInsightsView

urlpatterns = [
    path('summary/', AnalyticsSummaryView.as_view(), name='analytics-summary'),
    path('insights/', CareerInsightsView.as_view(), name='analytics-insights'),
]
