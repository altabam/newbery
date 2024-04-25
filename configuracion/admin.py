from django.contrib import admin
from configuracion.models import Personas, Socios, Disciplinas, Categorias, JugadoresCategoria, Becas
# Register your models here.
admin.site.register(Personas)
admin.site.register(Socios)
admin.site.register(Disciplinas)
admin.site.register(Categorias)
admin.site.register(JugadoresCategoria)
admin.site.register(Becas)
