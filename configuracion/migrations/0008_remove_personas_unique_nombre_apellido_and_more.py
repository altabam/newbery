# Generated by Django 4.2.11 on 2024-05-08 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0007_alter_personas_fecha_nacimiento"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="personas", name="unique_nombre_apellido",
        ),
        migrations.AddConstraint(
            model_name="personas",
            constraint=models.UniqueConstraint(
                fields=("nombre", "apellido", "dni"), name="unique_nombre_apellido_dni"
            ),
        ),
    ]
