# Generated by Django 4.2.11 on 2024-05-10 16:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("configuracion", "0009_socios_responsable"),
    ]

    operations = [
        migrations.RenameField(
            model_name="socios", old_name="personas", new_name="persona",
        ),
    ]
