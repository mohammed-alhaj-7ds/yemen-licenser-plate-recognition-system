"""
WSGI config for LPR project.
"""

import os
from django.core.wsgi import get_wsgi_application
print("DEBUG: Loading core.wsgi application...")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')
application = get_wsgi_application()
