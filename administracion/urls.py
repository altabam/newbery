from django.urls import path,re_path

from administracion.libreria.gest_backup import realizarBackup

app_name = 'administracion'
urlpatterns = [
    path("realizarBackup/<slug:slug>",realizarBackup, name="realizarBackup"),
]