from django.urls import path,re_path

from administracion.libreria.gest_backup import realizarBackup, gestionarBackup
from administracion.views import actualizarSecuenciaIdPersonas, envioEmail

app_name = 'administracion'
urlpatterns = [
    path("realizarBackup/<slug:slug>",realizarBackup, name="realizarBackup"),
    path("gestionarBackup",gestionarBackup, name="gestionarBackup"),
    path("actualizarSecuenciaIdPersonas",actualizarSecuenciaIdPersonas, name="actualizarSecuenciaIdPersonas"),
    path("envioEmail",envioEmail, name="envioEmail"),
]
