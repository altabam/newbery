from django.urls import path
from configuracion.views import listadoPersonas, listadoDisciplinas, listadoCategorias, listadoBecas, listadoJugadores, listadoSocios, cargaInicial,cargaMasivaSocios,cargaMasiva, borrarTodosSocios,borrarJugadoresCategoria, cargarJugadoresCategoria, gestionarJugadoresCategoria, cargarCategorias, cargaInicialDisciplinas, cargaInicialBecas, cargaInicialCategorias 
from configuracion.views import cargaInicialCuotas
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas"),
    path("listadoDisciplinas",listadoDisciplinas, name="listadoDisciplinas"),
    path("listadoCategorias",listadoCategorias, name="listadoCategorias"),
    path("listadoBecas",listadoBecas, name="listadoBecas"),
    path("listadoJugadores",listadoJugadores, name="listadoJugadores"),
    path("listadoSocios",listadoSocios, name="listadoSocios"),
    path("cargaInicial",cargaInicial, name="cargaInicial"),
    path("cargaInicialDisciplinas",cargaInicialDisciplinas, name="cargaInicialDisciplinas"),
    path("cargaInicialBecas",cargaInicialBecas, name="cargaInicialBecas"),
    path("cargaInicialCategorias",cargaInicialCategorias, name="cargaInicialCategorias"),
    path("cargaInicialCuotas",cargaInicialCuotas, name="cargaInicialCuotas"),
    path("cargaMasiva",cargaMasiva, name="cargaMasiva"),
    path("cargaMasivaSocios",cargaMasivaSocios, name="cargaMasivaSocios"),
    path("borrarTodosSocios",borrarTodosSocios, name="borrarTodosSocios"),
    path("borrarJugadoresCategoria/<int:id>",borrarJugadoresCategoria, name="borrarJugadoresCategoria"),
    path("cargarJugadoresCategoria/<int:id>",cargarJugadoresCategoria, name="cargarJugadoresCategoria"),
    path("gestionarJugadoresCategoria",gestionarJugadoresCategoria, name="gestionarJugadoresCategoria"),
   path("cargarCategorias",cargarCategorias, name="cargarCategorias"),

        
]