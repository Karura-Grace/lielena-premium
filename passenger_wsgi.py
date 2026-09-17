"""
Entry point for cPanel's "Setup Python App" (Phusion Passenger).

When you create a Python App in cPanel, it looks for a file called
passenger_wsgi.py in the app's root directory. This file just hands off
to Django's normal WSGI application — you shouldn't need to edit it.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lielena.settings')

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
