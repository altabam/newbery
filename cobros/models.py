from django.db import models
from configuracion.models import Socios, Disciplinas


# Create your models here.
class Pagos(models.Model):
    fecha_pago = models.DateField()
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE)
    monto = models.FloatField()
    

class DetallePagos(models.Model):
    MES = (
        ("ENE", "Enero"),
        ("FEB", "Febrero"),
        ("MAR", "Marzo"),
        ("ABR", "Abril"),
        ("MAY", "Mayo"),
        ("JUN", "Junio"),
        ("JUL", "Julio"),
        ("AGO", "Agosto"),
        ("SEP", "Septiembre"),
        ("OCT", "Octubre"),
        ("NOV", "Noviembre"),
        ("DIC", "Diciembre"),
    )
    anio =  models.CharField(max_length=4)
    mes = models.CharField(max_length=3, choices=MES, blank=True)
    pago = models.ForeignKey(Pagos, on_delete=models.CASCADE)


class SituacionInicial(models.Model):
    anio =  models.IntegerField()
    mes = models.IntegerField( )
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)

 