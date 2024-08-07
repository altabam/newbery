# Generated by Django 4.2.11 on 2024-08-01 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0020_categorias_activo'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='jugadores',
            name='unique_player_category_period',
        ),
        migrations.AddConstraint(
            model_name='jugadores',
            constraint=models.UniqueConstraint(fields=('persona', 'categoria', 'fecha_desde'), name='unique_player_category_period'),
        ),
    ]
