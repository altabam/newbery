# Generated by Django 4.2.11 on 2024-05-09 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0008_remove_personas_unique_nombre_apellido_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="socios",
            name="responsable",
            field=models.CharField(
                blank=True,
                choices=[("S", "SI"), ("N", "NO")],
                default="N",
                max_length=1,
            ),
        ),
    ]