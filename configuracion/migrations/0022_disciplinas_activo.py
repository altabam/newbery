# Generated by Django 4.2.11 on 2024-08-07 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0021_remove_jugadores_unique_player_category_period_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplinas',
            name='activo',
            field=models.BooleanField(default=True),
        ),
    ]