"""
WSGI config for mez4proj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from mezzanine.utils.conf import real_project_name


os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f'{real_project_name("geany")}.settings')

application = get_wsgi_application()
