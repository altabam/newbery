from django.db import models

# Create your models here.
class Socios(models.Model):
    numero = models.IntegerField()


class Personas(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dni = models.IntegerField()
    socio = models.ForeignKey(Socios, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    

class Disciplinas(models.Model):
    nombre = models.CharField(max_length=100)

class Categorias (models.Model):
    nombre = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre}"


class JugadoresCategoria(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)


class Beca(models.Model):
    nombre = models.CharField(max_length=100)
    porcentaje = models.FloatField()