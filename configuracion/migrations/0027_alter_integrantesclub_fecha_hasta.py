# Generated by Django 4.2.11 on 2025-01-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0026_remove_integrantesclub_persona_integrantesclub_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrantesclub',
            name='fecha_hasta',
            field=models.DateField(blank=True, null=True),
        ),
    ]
