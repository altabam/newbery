from django.urls import path
from configuracion.views import listadoPersonas, listadoDisciplinas, listadoCategorias, listadoBecas, listadoJugadores, cargaInicial
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas"),
    path("listadoDisciplinas",listadoDisciplinas, name="listadoDisciplinas"),
    path("listadoCategorias",listadoCategorias, name="listadoCategorias"),
    path("listadoBecas",listadoBecas, name="listadoBecas"),
    path("listadoJugadores",listadoJugadores, name="listadoJugadores"),
    path("cargaInicial",cargaInicial, name="cargaInicial"),
]