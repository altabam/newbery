# Generated by Django 4.2.11 on 2025-03-05 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0029_integrantesclubcategorias_delete_asistencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaracteristicaEvaluar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caracteristica', models.CharField(max_length=250)),
            ],
        ),
    ]
