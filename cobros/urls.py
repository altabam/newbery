from django.urls import path
from cobros.views import render_cobros, verPagoSocio


urlpatterns = [
    path("",render_cobros, name="cobros"),
    path('verPagoSocio/<int:id>',verPagoSocio, name='verPagoSocio'),
    
]