from django.db import models

# Create your models here.


class ValidacionEmail(models.Model):

    codigo = models.IntegerField()
    email = models.CharField(max_length=254)
    fecha_alta = models.DateField(null=True)
    fecha_uso = models.DateField(null=True)
    def __str__(self):
        return f"{self.codigo} {self.email} {self.fecha_alta} {self.fecha_baja}"

