from django.urls import path
from cobros.views import render_cobros
urlpatterns = [
    path("render_cobros/",render_cobros, name="cobros")
]