# Generated by Django 4.2.11 on 2024-04-29 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0004_delete_jugadorescategoria"),
    ]

    operations = [
        migrations.AddField(
            model_name="personas",
            name="direccion",
            field=models.CharField(default=" ", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="personas",
            name="telefono",
            field=models.CharField(default="1111", max_length=15),
            preserve_default=False,
        ),
    ]