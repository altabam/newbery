from django.urls import path
from configuracion.views import listadoDisciplinas, listadoCategorias, listadoBecas, listadoJugadores, listadoSocios, listarCuotas
from configuracion.views import cargaInicial,cargaMasivaSocios,cargaMasiva, borrarTodosSocios,borrarJugadoresCategoria, cargarJugadoresCategoria, gestionarJugadoresCategoria, cargarCategorias, cargaInicialDisciplinas, cargaInicialBecas, cargaInicialCategorias 
from configuracion.views import cargaInicialCuotas, cargarAgrupacionFamiliarSocios, borrarSocio
from configuracion.views import listadoPersonas, borrarPersona, editarPersona,agregarPersona
from configuracion.libreria.gest_socios import agruparSocios
app_name = 'configuracion'
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas"),
    path("listadoDisciplinas",listadoDisciplinas, name="listadoDisciplinas"),
    path("listadoCategorias",listadoCategorias, name="listadoCategorias"),
    path("listadoBecas",listadoBecas, name="listadoBecas"),
    path("listadoJugadores",listadoJugadores, name="listadoJugadores"),
    path("listadoSocios",listadoSocios, name="listadoSocios"),
    path("listarCuotas",listarCuotas, name="listarCuotas"),
    path("cargaInicial",cargaInicial, name="cargaInicial"),
    path("cargaInicialDisciplinas",cargaInicialDisciplinas, name="cargaInicialDisciplinas"),
    path("cargaInicialBecas",cargaInicialBecas, name="cargaInicialBecas"),
    path("cargaInicialCategorias",cargaInicialCategorias, name="cargaInicialCategorias"),
    path("cargaInicialCuotas",cargaInicialCuotas, name="cargaInicialCuotas"),
    path("cargaMasiva",cargaMasiva, name="cargaMasiva"),
    path("cargaMasivaSocios",cargaMasivaSocios, name="cargaMasivaSocios"),
    path("cargarAgrupacionFamiliarSocios",cargarAgrupacionFamiliarSocios, name="cargarAgrupacionFamiliarSocios"),
    path("borrarTodosSocios",borrarTodosSocios, name="borrarTodosSocios"),
    path("borrarSocio/<int:id>",borrarSocio, name="borrarSocio"),
    path("borrarJugadoresCategoria/<int:id>",borrarJugadoresCategoria, name="borrarJugadoresCategoria"),
    path("cargarJugadoresCategoria/<int:id>",cargarJugadoresCategoria, name="cargarJugadoresCategoria"),
    path("gestionarJugadoresCategoria",gestionarJugadoresCategoria, name="gestionarJugadoresCategoria"),
    path("cargarCategorias",cargarCategorias, name="cargarCategorias"),
    path("editarPersona/<int:id>",editarPersona, name="editarPersona"),
    path("borrarPersona/<int:id>",borrarPersona, name="borrarPersona"),
    path('agregarPersona/',agregarPersona, name='agregarPersona'),
    path('agruparSocios/',agruparSocios, name='agruparSocios'),
  

        
]