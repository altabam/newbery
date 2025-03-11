# Generated by Django 4.2.11 on 2025-03-07 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0030_caracteristicaevaluar'),
        ('gestJugadores', '0002_evaltecnicotacticaactitudinal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evaltecnicotacticaactitudinaljugador',
            name='tipoEvaluacion',
        ),
        migrations.CreateModel(
            name='EvalTecnicoTacticaActitudinalCaracteristica',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('carteristicaEvaluar', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.caracteristicaevaluar')),
                ('tipoEvaluacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestJugadores.evaltecnicotacticaactitudinal')),
            ],
        ),
        migrations.AlterField(
            model_name='evaltecnicotacticaactitudinaljugador',
            name='carteristicaEvaluar',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestJugadores.evaltecnicotacticaactitudinalcaracteristica'),
        ),
    ]
