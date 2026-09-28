"""
Development settings for LinkedInCareerPilot AI backend.
"""

from .base import *
import os

DEBUG = True

ALLOWED_HOSTS = ['*']

# Database: SQLite3 by default in development; if DATABASE_URL is set, parse with dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    try:
        import dj_database_url
        DATABASES['default'] = dj_database_url.parse(DATABASE_URL)
    except Exception as e:
        print(f"Warning: Could not connect via DATABASE_URL ({e}), defaulting to SQLite3.")

# Development Email Backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CORS Settings for local frontend (React + Vite port 5173, Next.js port 3000)
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

AUTH_PASSWORD_VALIDATORS = []
