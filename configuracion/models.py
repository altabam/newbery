from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class PersonasManager(models.Manager):
    def get_by_natural_key(self, nombre, apellido,dni):
        return self.get(nombre=nombre, apellido=apellido, dni=dni)
    
class Personas(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField(null=True)
    dni = models.IntegerField()
    telefono  = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)

    objects = PersonasManager()
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
    def natural_key(self):
        return (self.nombre, self.apellido, self.dni)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["nombre", "apellido","dni"],
                name="unique_nombre_apellido_dni",
            ),
        ]
    
    
class Socios(models.Model):
    SOCIO_RESPONSABLE = (
        ("S", "SI"),
        ("N", "NO"),
    )
    numero = models.IntegerField()
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    responsable = models.CharField(max_length=1, choices=SOCIO_RESPONSABLE, blank=True, default='N')
    fecha_alta = models.DateField(null=True)
    fecha_baja= models.DateField(null=True)
    def __str__(self):
        return f"{self.numero} {self.persona.apellido} {self.persona.nombre}"


class Disciplinas(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    activo = models.BooleanField(default=True)  # Campo para la eliminación lógica
    def __str__(self):
        return self.nombre

class Categorias (models.Model):
    nombre = models.CharField(max_length=100)
    disciplina = models.ForeignKey(Disciplinas, on_delete=models.CASCADE)
    paga_disciplina = models.BooleanField(default="True")
    activo = models.BooleanField(default=True)  # Campo para la eliminación lógica
    def __str__(self):
        return f"{self.nombre}"


class Jugadores(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE)
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    activo = models.BooleanField(default=True)  # Campo para la eliminación lógica
    def __str__(self):
        return f"{self.persona} - {self.categoria}"

    def clean(self):
        if not self.persona or not self.categoria:
            # Si persona o categoria no están definidos, no podemos hacer la validación
            return

        disciplina = self.categoria.disciplina
        if disciplina:
            overlap= Jugadores.objects.filter(
                persona=self.persona,
                categoria=self.categoria,
                activo=True,
                fecha_desde=self.fecha_desde
            ).exclude(id=self.id)
            for jugador in overlap:
                if (
                    (jugador.fecha_hasta is None or jugador.fecha_hasta >= self.fecha_desde) and
                    (self.fecha_hasta is None or self.fecha_hasta >= jugador.fecha_desde)
                ):
                    raise ValidationError('El jugador ya está activo en esta categoría y disciplina dentro del mismo periodo de tiempo.')

    def save(self, *args, **kwargs):
        # Llamar a la validación antes de guardar
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(#asegura que la restricción se respete directamente en base de datos
                fields=['persona', 'categoria', 'fecha_desde'],
                name='unique_player_category_period'
            )
        ]

class Becas(models.Model):
    nombre = models.CharField(max_length=100)
    porcentaje = models.FloatField()
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    activo = models.BooleanField(default=True)  # Campo para la eliminación lógica

class Cuotas(models.Model):
    concepto = models.CharField(max_length=100)
    valor = models.DecimalField( max_digits=9, decimal_places=2) 
    cant_int = models.IntegerField()
    fecha_desde = models.DateField(null=True)
    fecha_hasta= models.DateField(null=True)

class BecasMotivos(models.Model):
    concepto = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.concepto}"



class CalidadIntegrante(models.Model):
    concepto = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.concepto}"


class IntegrantesClub(models.Model):
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    calidad = models.ForeignKey(CalidadIntegrante, on_delete=models.CASCADE)
    fecha_desde =models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)

class BecasJugador(models.Model):
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
    jugador = models.ForeignKey(Jugadores, on_delete=models.CASCADE)
    beca = models.ForeignKey(Becas, on_delete=models.CASCADE)
    anio =  models.CharField(max_length=4)
    mesDesde = models.CharField(max_length=3, choices=MES, blank=True)
    mesHasta = models.CharField(max_length=3, choices=MES, blank=True)
    motivoSolicitud =models.ForeignKey(BecasMotivos, on_delete=models.CASCADE, blank=True)
    solicita = models.ForeignKey(IntegrantesClub, on_delete=models.CASCADE)

    