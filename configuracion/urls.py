from django.urls import path,re_path
from configuracion.views import listadoDisciplinas, listadoCategorias, listadoBecas, listadoJugadores, listadoSocios, listarCuotas
# pasar todo este from a gest_carga_inicial.py
from configuracion.views import cargaInicial,cargaMasivaSocios,cargaMasiva, borrarTodosSocios
from configuracion.views import borrarJugadoresCategoria, cargarJugadoresCategoria, gestionarJugadoresCategoria, listarJugadoresNoSocios
from configuracion.views import cargarCategorias, cargaInicialDisciplinas, cargaInicialBecas, cargaInicialCategorias 
from configuracion.views import cargarAgrupacionFamiliarSocios, borrarSocio
from configuracion.views import listarMotivoBecas, cargaBecasJugador
from configuracion.views import listarMotivoCalicadIntegrantes, listarIntegrantesClub
from configuracion.views import listadoPersonas, borrarPersona, editarPersona,agregarPersona,agregarDisciplinas,editarDisciplinas,borrarLogDisciplinas,borrarDisciplinas, agregarCategorias, editarCategorias,borrarLogCategorias,borrarCategorias, agregarJugadorCategorias, editarJugadorCategorias,borrarJugadorLogCategorias, borrarJugadorCategorias
from configuracion.views import obtenerCategorias,obtener_personas
from configuracion.libreria.gest_socios import agruparSocios, buscarSocio, buscarSocioResponsable,listarIntegrantesSocios,agregarIntegranteSocio, listarIntegrantesSinSocio, quitarIntegranteSocio, listarPersonasNoSocios,agregarNuevoSocio, eliminarSocioResponsable
from configuracion.libreria.gest_carga_inicial import cargaInicialMotivosBeca, cargaInicialCalidadIntegrante, cargaInicialCuotas
from configuracion.libreria.cargaMasiva import cargaIntegrantesClub, cargaBecasJugadores
from configuracion.libreria.gest_becas import listarBecados
from configuracion.libreria.gest_personas import buscarPersona
from configuracion.libreria.reportes import reportes, reporteJugadoresPorDisciplina, reporteJugadoresPorCategoria
from configuracion.libreria.gest_integrante_club import agregarIntegranteClub, gestionarIntegranteClub, borrarIntegranteClub, editarIntegranteClub
from configuracion.libreria.gest_jugadores import generarPdfJugadores
from configuracion.views import generarSecuencia
app_name = 'configuracion'
urlpatterns = [
    path("listadoPersonas",listadoPersonas, name="listadoPersonas"),
    path("listadoDisciplinas",listadoDisciplinas, name="listadoDisciplinas"),
    path("listadoCategorias",listadoCategorias, name="listadoCategorias"),
    path("listadoBecas",listadoBecas, name="listadoBecas"),
    path("listadoJugadores",listadoJugadores, name="listadoJugadores"),
    path("generarPdfJugadores",generarPdfJugadores.as_view(), name="generarPdfJugadores"),
    
    path("listadoSocios",listadoSocios, name="listadoSocios"),
    path("listarCuotas",listarCuotas, name="listarCuotas"),
    path("listarIntegrantesClub",listarIntegrantesClub, name="listarIntegrantesClub"),
    path("listarMotivoCalicadIntegrantes",listarMotivoCalicadIntegrantes, name="listarMotivoCalicadIntegrantes"),
    path("listarMotivoBecas",listarMotivoBecas, name="listarMotivoBecas"),
    path("cargaInicial",cargaInicial, name="cargaInicial"),
    path("cargaInicialDisciplinas",cargaInicialDisciplinas, name="cargaInicialDisciplinas"),
    path("cargaInicialBecas",cargaInicialBecas, name="cargaInicialBecas"),
    path("cargaInicialBecas",cargaInicialBecas, name="cargaInicialBecas"),
    path("cargaInicialMotivosBeca",cargaInicialMotivosBeca, name="cargaInicialMotivosBeca"),
    path("cargaInicialCalidadIntegrante",cargaInicialCalidadIntegrante, name="cargaInicialCalidadIntegrante"),
    path("cargaInicialCategorias",cargaInicialCategorias, name="cargaInicialCategorias"),
    path("cargaInicialCuotas",cargaInicialCuotas, name="cargaInicialCuotas"),
    path("cargaIntegrantesClub",cargaIntegrantesClub, name="cargaIntegrantesClub"),
    path("cargaBecasJugadores",cargaBecasJugadores, name="cargaBecasJugadores"),
    path("cargaMasiva",cargaMasiva, name="cargaMasiva"),
    path("cargaMasivaSocios",cargaMasivaSocios, name="cargaMasivaSocios"),
    path("cargarAgrupacionFamiliarSocios",cargarAgrupacionFamiliarSocios, name="cargarAgrupacionFamiliarSocios"),
    path("borrarTodosSocios",borrarTodosSocios, name="borrarTodosSocios"),
    path("borrarSocio/<int:id>",borrarSocio, name="borrarSocio"),
    path("borrarJugadorLogCategorias/<int:id>",borrarJugadorLogCategorias, name="borrarJugadorLogCategorias"),
    path("borrarJugadoresCategorias/<int:id>",borrarJugadoresCategoria, name="borrarJugadoresCategoria"),
    path("cargarJugadoresCategoria/<int:id>",cargarJugadoresCategoria, name="cargarJugadoresCategoria"),
    path("gestionarJugadoresCategoria",gestionarJugadoresCategoria, name="gestionarJugadoresCategoria"),
    path("cargarCategorias",cargarCategorias, name="cargarCategorias"),
    path("editarPersona/<int:id>",editarPersona, name="editarPersona"),
    path("editarDisciplinas/<int:id>",editarDisciplinas, name="editarDisciplinas"),
    path("editarCategorias/<int:id>",editarCategorias, name="editarCategorias"),
    path("editarJugadorCategorias/<int:id>",editarJugadorCategorias, name="editarJugadorCategorias"),
    path("borrarPersona/<int:id>",borrarPersona, name="borrarPersona"),
    path("borrarLogDisciplinas/<int:id>",borrarLogDisciplinas, name="borrarLogDisciplinas"),
    path("borrarDisciplinas/<int:id>",borrarDisciplinas, name="borrarDisciplinas"),
    path("borrarCategorias/<int:id>",borrarCategorias, name="borrarCategorias"),
    path("borrarLogCategorias/<int:id>",borrarLogCategorias, name="borrarLogCategorias"),
    path("borrarJugadorCategorias/<int:id>",borrarJugadorCategorias, name="borrarJugadorCategorias"),
    path('agregarPersona/',agregarPersona, name='agregarPersona'),
    path('agregarDisciplinas/',agregarDisciplinas, name='agregarDisciplinas'),
    path('agregarCategorias/', agregarCategorias, name='agregarCategorias'),
    path('agregarJugadorCategorias/', agregarJugadorCategorias, name='agregarJugadorCategorias'),
    path('agruparSocios/',agruparSocios, name='agruparSocios'),
    path('listarIntegrantesSocios/<int:id>',listarIntegrantesSocios, name='listarIntegrantesSocios'),
    path('listarIntegrantesSinSocio/<int:id>',listarIntegrantesSinSocio, name='listarIntegrantesSinSocio'),
    path('listarBecados',listarBecados, name='listarBecados'),
    
    path('agregarJugadorCategorias/obtenerCategorias/', obtenerCategorias, name='obtenerCategorias'),
    path('editarJugadorCategorias/obtenerCategorias/', obtenerCategorias, name='obtenerCategorias'),
    path('obtener_personas/', obtener_personas, name='obtener_personas'),
    path('listarJugadoresNoSocios/', listarJugadoresNoSocios, name='listarJugadoresNoSocios'),

    path('agregarIntegranteSocio/<int:id>/<int:idpk>',agregarIntegranteSocio, name='agregarIntegranteSocio'),
    path('agregarNuevoSocio/<int:id>/',agregarNuevoSocio, name='agregarNuevoSocio'),
    path('eliminarSocioResponsable/<int:id>/',eliminarSocioResponsable, name='eliminarSocioResponsable'),
    path('listarPersonasNoSocios/',listarPersonasNoSocios, name='listarPersonasNoSocios'),
    path('quitarIntegranteSocio/<int:id>/<int:idpk>',quitarIntegranteSocio, name='quitarIntegranteSocio'),

    path('cargaBecasJugador',cargaBecasJugador, name='cargaBecasJugador'),
    
    re_path(r'^buscarPersona/$', buscarPersona, name='buscarPersona'),
    re_path(r'^buscarSocio/$', buscarSocio, name='busquedaSocio'), 
    re_path(r'^buscarSocioResponsable/',buscarSocioResponsable, name='buscarSocioResponsable'),


    path('secuencia/<slug:slug>/<int:id>',generarSecuencia, name='generarSecuencia'),

    path('reporteJugadoresPorDisciplina',reporteJugadoresPorDisciplina, name='reporteJugadoresPorDisciplina'),
    path('reporteJugadoresPorCategoria',reporteJugadoresPorCategoria, name='reporteJugadoresPorCategoria'),

    path('agregarIntegranteClub/', agregarIntegranteClub, name='agregarIntegranteClub'),
    path("borrarIntegranteClub/<int:id>",borrarIntegranteClub, name="borrarIntegranteClub"),
    path("editarIntegranteClub/<int:id>",editarIntegranteClub, name="editarIntegranteClub"),

    path('reportes',reportes, name='reportes'),

        
]