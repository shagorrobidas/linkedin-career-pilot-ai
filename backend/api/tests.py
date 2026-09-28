from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.core.management import call_command

from accounts.models import User
from jobs.models import Job
from applications.models import JobApplication


class LinkedInCareerPilotAPITests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Run seed_data to populate test database
        call_command('seed_data')

    def setUp(self):
        self.client = APIClient()
        # Login with seeded demo user
        response = self.client.post('/api/v1/auth/login/', {
            'email': 'demo@linkedincareerpilot.ai',
            'password': 'Password123!'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data['data'])
        self.token = response.data['data']['access_token']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_auth_login_invalid(self):
        client = APIClient()
        response = client.post('/api/v1/auth/login/', {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_register(self):
        client = APIClient()
        response = client.post('/api/v1/auth/register/', {
            'email': 'newuser@example.com',
            'password': 'StrongPassword123!',
            'first_name': 'Jane',
            'last_name': 'Developer'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('access_token', response.data['data'])
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_dashboard_overview(self):
        response = self.client.get('/api/v1/dashboard/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreaterEqual(response.data['data']['jobs_discovered'], 1)

    def test_jobs_list(self):
        response = self.client.get('/api/v1/jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertGreaterEqual(response.data['count'], 1)

    def test_jobs_analyze(self):
        job = Job.objects.first()
        self.assertIsNotNone(job)
        response = self.client.post(f'/api/v1/jobs/{job.id}/analyze/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('match_score', response.data['data'])

    def test_applications_update_status(self):
        app = JobApplication.objects.first()
        self.assertIsNotNone(app)
        response = self.client.patch(f'/api/v1/applications/{app.id}/update_status/', {
            'status': JobApplication.Status.INTERVIEW
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        app.refresh_from_db()
        self.assertEqual(app.status, JobApplication.Status.INTERVIEW)

    def test_content_generate(self):
        response = self.client.post('/api/v1/content/generate/', {
            'topic': 'High Performance Django REST APIs',
            'tone': 'PROFESSIONAL'
        }, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertTrue(response.data['success'])

    def test_agents_list(self):
        response = self.client.get('/api/v1/agents/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_profile_health(self):
        response = self.client.get('/api/v1/profile/health/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('overall_health_score', response.data['data'])

    def test_openapi_schema(self):
        response = self.client.get('/api/schema/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
