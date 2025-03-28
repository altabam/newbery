# Generated by Django 4.2.11 on 2025-02-11 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracion', '0029_integrantesclubcategorias_delete_asistencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='AsistenciaEventoDeportivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('asiste', models.CharField(blank=True, choices=[('S', 'SI'), ('N', 'NO')], default='N', max_length=1)),
                ('observaciones', models.CharField(blank=True, max_length=255)),
                ('justifica', models.CharField(blank=True, choices=[('S', 'SI'), ('N', 'NO')], default='N', max_length=1)),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.eventodeportivo')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.jugadores')),
            ],
        ),
    ]
