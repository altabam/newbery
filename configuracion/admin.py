from django.contrib import admin
from configuracion.models import Personas, Socios, Disciplinas, Categorias, Jugadores, Becas,IntegrantesClub,CalidadIntegrante,EventoDeportivo,IntegrantesClubCategorias,CaracteristicaEvaluar
# Register your models here.
admin.site.register(Personas)
admin.site.register(Socios)
admin.site.register(Disciplinas)
admin.site.register(Categorias)
admin.site.register(Jugadores)
admin.site.register(Becas)
admin.site.register(IntegrantesClub)
admin.site.register(CalidadIntegrante)
admin.site.register(EventoDeportivo)
admin.site.register(IntegrantesClubCategorias)
admin.site.register(CaracteristicaEvaluar)

