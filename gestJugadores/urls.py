from django.urls import path,re_path
from .views import cargarAsistencia,filtrarJugadoresCategoria,cargarAsistenciaJugadoresCategoria,listarAsistencia,filtrarAsistenciaJugadoresCategoria
app_name = 'gestJugadores'
urlpatterns = [
    path("cargarAsistencia/<int:anio>/<int:mes>/<int:dia>/<int:categoria>/<slug:fechaEntrenamiento>/<int:evento>",cargarAsistencia, name="cargarAsistencia"),
    path("filtrarJugadoresCategoria",filtrarJugadoresCategoria, name="filtrarJugadoresCategoria"),
    path("cargarAsistenciaJugadoresCategoria/<int:categoria>/<slug:fechaEntrenamiento>",cargarAsistenciaJugadoresCategoria, name="cargarAsistenciaJugadoresCategoria"),
    path("listarAsistencia",listarAsistencia, name="listarAsistencia"),
    path("filtrarAsistenciaJugadoresCategoria",filtrarAsistenciaJugadoresCategoria, name="filtrarAsistenciaJugadoresCategoria"),
    path("filtrarAsistenciaJugadoresCategoria/<int:anio>/<int:mes>/<int:accion>/<int:categoria>/<slug:fechaEntrenamiento>/<int:evento>",filtrarAsistenciaJugadoresCategoria, name="filtrarAsistenciaJugadoresCategoria"),

    
    

        
]