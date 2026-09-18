"""
Entry point for Vercel's Python runtime.

Vercel's @vercel/python builder looks for a WSGI-compatible callable named
`app` in this file. This just hands off to Django's normal WSGI app —
you shouldn't need to edit this file.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lielena.settings')

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
