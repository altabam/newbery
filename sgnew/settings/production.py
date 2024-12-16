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




EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Por ejemplo, 'smtp.gmail.com' para Gmail
EMAIL_PORT = 587  # Usualmente 587 para TLS
EMAIL_USE_TLS = True  # Habilitar TLS
EMAIL_HOST_USER = 'altabam@gmail.com'  # Tu dirección de correo
EMAIL_HOST_PASSWORD = 'G00gle123'  # Contraseña de tu cuenta
DEFAULT_FROM_EMAIL = 'altabam@gmail.com'