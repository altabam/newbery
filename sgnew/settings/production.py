from .base import *


DEBUG = False

ALLOWED_HOSTS = []


DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}


CSRF_TRUSTED_ORIGINS = [
    "https://newbery-production.up.railway.app",
]