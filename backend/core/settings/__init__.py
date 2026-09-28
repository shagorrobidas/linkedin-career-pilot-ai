"""
Settings package initialization.
Defaults to development settings if DJANGO_ENV is not specified.
"""

import os

env = os.environ.get('DJANGO_ENV', 'development').lower()

if env == 'production':
    from .production import *
else:
    from .development import *
