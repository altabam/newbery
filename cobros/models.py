from django.db import models
from configuracion.models import Socios

# Create your models here.
class Cobros(models.Model):
    fecha_cobro = models.DateField()
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE)
    monto = models.FloatField()