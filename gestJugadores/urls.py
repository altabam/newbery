from django.urls import path,re_path
from .views import cargarAsistencia
app_name = 'gestJugadores'
urlpatterns = [
    path("cargarAsistencia",cargarAsistencia, name="cargarAsistencia"),

        
]