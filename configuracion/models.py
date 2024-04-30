from django.db import models

# Create your models here.


class Personas(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    dni = models.IntegerField()
    telefono  = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    
class Socios(models.Model):
    numero = models.IntegerField()
    personas = models.ForeignKey(Personas, on_delete=models.CASCADE)

class Disciplinas(models.Model):
    nombre = models.CharField(max_length=100)

class Categorias (models.Model):
    nombre = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre}"


class Jugadores(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)

class Becas(models.Model):
    nombre = models.CharField(max_length=100)
    porcentaje = models.FloatField()