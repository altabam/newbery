# Generated by Django 4.2.11 on 2025-03-05 16:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0030_caracteristicaevaluar'),
        ('gestJugadores', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvalTecnicoTacticaActitudinal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('anio', models.SmallIntegerField()),
                ('mes', models.SmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EvalTecnicoTacticaActitudinalJugador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, null=True)),
                ('evaluacion', models.CharField(blank=True, choices=[('A', 'Alto 10 a 8'), ('M', 'Medio 7 a 5'), ('B', 'Bajo 4 a 1'), ('N', 'No Evaluado')], default='N', max_length=1)),
                ('observaciones', models.CharField(blank=True, max_length=255)),
                ('carteristicaEvaluar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.caracteristicaevaluar')),
                ('evaluador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.integrantesclub')),
                ('jugador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.jugadores')),
                ('tipoEvaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestJugadores.evaltecnicotacticaactitudinal')),
            ],
        ),
    ]
