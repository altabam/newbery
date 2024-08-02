from django.urls import path
from cobros.views import render_cobros, verPagoSocio,listarSitInicial, agregarSitInicial, editarSitInicial, borrarSitInicial, listarSociosDeuda, pagarCuota
app_name = 'cobros'

urlpatterns = [
    path("",render_cobros, name="cobros"),
    path('verPagoSocio/<int:id>',verPagoSocio, name='verPagoSocio'),
    path('agregarSitInicial/',agregarSitInicial, name='agregarSitInicial'),
    path("editarSitInicial/<int:id>",editarSitInicial, name="editarSitInicial"),
    path("borrarSitInicial/<int:id>",borrarSitInicial, name="borrarSitInicial"),
    path("listarSitInicial",listarSitInicial, name="listarSitInicial"),
    path("listarSociosDeuda",listarSociosDeuda, name="listarSociosDeuda"),
    path('pagarCuota/',pagarCuota, name='pagarCuota'),

    
    
    
]