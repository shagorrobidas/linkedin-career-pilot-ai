from rest_framework.views import APIView
from rest_framework.response import Response
from analytics.models import CareerInsight
from analytics.api.serializers import CareerInsightSerializer


class AnalyticsSummaryView(APIView):
    def get(self, request):
        return Response({
            'success': True,
            'data': {
                'applications_trend': [
                    {'date': '2026-09-20', 'applications': 2, 'interviews': 0},
                    {'date': '2026-09-21', 'applications': 5, 'interviews': 1},
                    {'date': '2026-09-22', 'applications': 4, 'interviews': 0},
                    {'date': '2026-09-23', 'applications': 6, 'interviews': 2},
                    {'date': '2026-09-24', 'applications': 3, 'interviews': 1},
                    {'date': '2026-09-25', 'applications': 4, 'interviews': 0},
                ],
                'post_impressions_weekly': 4280,
                'high_match_percentage': 78,
                'ai_credits_used_this_week': 24
            }
        })


class CareerInsightsView(APIView):
    def get(self, request):
        insights = CareerInsight.objects.all()
        if insights.exists():
            data = CareerInsightSerializer(insights, many=True).data
        else:
            data = [
                {
                    'category': 'SKILL_GAP',
                    'title': 'High Demand for Distributed Systems Knowledge',
                    'description': '85% of your high-match backend roles list Redis clustering and Celery architecture.',
                    'actionable_step': 'Publish a LinkedIn post detailing your experience building distributed task queues.'
                },
                {
                    'category': 'PROFILE_STRENGTH',
                    'title': 'Strong Match on Python and Django',
                    'description': 'Your match score averages 94% on Python/DRF engineering roles.',
                    'actionable_step': 'Highlight your API performance tuning accomplishments.'
                }
            ]
        return Response({
            'success': True,
            'data': data
        })
