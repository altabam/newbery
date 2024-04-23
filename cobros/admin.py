from django.contrib import admin
from cobros.models import Personas, Socios,  Categorias, JugadoresCategoria

# Register your models here.
admin.site.register(Personas)
admin.site.register(Socios)
admin.site.register(Categorias)
admin.site.register(JugadoresCategoria)
