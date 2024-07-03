from .base import *


DEBUG = True

ALLOWED_HOSTS = [ 
    "newbery-production.up.railway.app",
    "localhost"
]


DATABASES = {
    "default": dj_database_url.config(default=os.getenv("DATABASE_URL"))
}


CSRF_TRUSTED_ORIGINS = [
    "https://newbery-production.up.railway.app",
]