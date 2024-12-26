from .base import *


DEBUG = True

ALLOWED_HOSTS = [ 
    "newbery-production.up.railway.app",
    "localhost",
]


DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}


CSRF_TRUSTED_ORIGINS = [
    "https://newbery-production.up.railway.app",
]




EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS") 
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD") 
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")