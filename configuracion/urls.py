from django.urls import path
from configuracion.views import listadoPersonas
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas")
]