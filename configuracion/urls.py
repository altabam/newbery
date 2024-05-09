from django.urls import path
from configuracion.views import listadoPersonas, listadoDisciplinas, listadoCategorias, listadoBecas, listadoJugadores, listadoSocios, cargaInicial,cargaMasivaSocios,cargaMasiva
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas"),
    path("listadoDisciplinas",listadoDisciplinas, name="listadoDisciplinas"),
    path("listadoCategorias",listadoCategorias, name="listadoCategorias"),
    path("listadoBecas",listadoBecas, name="listadoBecas"),
    path("listadoJugadores",listadoJugadores, name="listadoJugadores"),
    path("listadoSocios",listadoSocios, name="listadoSocios"),
    path("cargaInicial",cargaInicial, name="cargaInicial"),
    path("cargaMasiva",cargaMasiva, name="cargaMasiva"),
    path("cargaMasivaSocios",cargaMasivaSocios, name="cargaMasivaSocios"),

        
]