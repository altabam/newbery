from django.urls import path, re_path
from cobros.views import render_cobros, busqueda_socio

urlpatterns = [
    path("",render_cobros, name="cobros"),
    re_path(r'^busquedaSocio/$', busqueda_socio, name='busquedaSocio'), 
]