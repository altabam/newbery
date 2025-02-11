from django.db import models

from configuracion.models import EventoDeportivo, Jugadores

# Create your models here.
class AsistenciaEventoDeportivo(models.Model):
    ASISTE = (
        ("S", "SI"),
        ("N", "NO"),
    )
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE)
    evento = models.ForeignKey(EventoDeportivo, on_delete= models.CASCADE)
    fecha = models.DateField(null=True,blank=True)
    asiste = models.CharField(max_length=1, choices=ASISTE, blank=True, default='N')
    observaciones= models.CharField(max_length=255,  blank=True)
    justifica = models.CharField(max_length=1, choices=ASISTE, blank=True, default='N')
