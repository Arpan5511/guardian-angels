"""
WSGI config for guardian_angels project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guardian_angels.settings')

application = get_wsgi_application()
