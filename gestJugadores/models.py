from django.db import models

from configuracion.models import EventoDeportivo, Jugadores, CaracteristicaEvaluar,IntegrantesClub

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

    
class EvalTecnicoTacticaActitudinal(models.Model):
    nombre = models.CharField(max_length=100)
    anio= models.SmallIntegerField()
    mes = models.SmallIntegerField()
    fechaInicio = models.DateField()
    fechaFin = models.DateField()

class EvalTecnicoTacticaActitudinalCaracteristica(models.Model):
    tipoEvaluacion = models.ForeignKey(EvalTecnicoTacticaActitudinal, on_delete=models.CASCADE)
    carateristicaEvaluar = models.ForeignKey(CaracteristicaEvaluar, on_delete= models.CASCADE)
    def __str__(self):
        return f"{self.carateristicaEvaluar, self.tipoEvaluacion.nombre}"


class EvalTecnicoTacticaActitudinalJugador(models.Model):
    VALOR = (
        ("A", "Alto 10 a 8"),
        ("M", "Medio 7 a 5"),
        ("B", "Bajo 4 a 1"),
        ("N", "No Evaluado"),
    )
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE)
    caracteristicaEvaluar = models.ForeignKey(EvalTecnicoTacticaActitudinalCaracteristica, on_delete= models.CASCADE)
    fecha = models.DateField(null=True,blank=True)
    evaluacion =  models.CharField(max_length=1, choices=VALOR, blank=True, default='N')
    observaciones= models.CharField(max_length=255,  blank=True)
    evaluador = models.ForeignKey(IntegrantesClub, on_delete= models.CASCADE)

