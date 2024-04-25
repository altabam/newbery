"""
ASGI config for sgnew project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from dotenv import load_dotenv

load_dotenv()

from django.core.asgi import get_asgi_application

"""os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sgnew.settings.local")"""
os.environ.setdefault("DJANGO_SETTINGS_MODULE", os.getenv("SETTING"))
application = get_asgi_application()
