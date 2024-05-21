# Generated by Django 4.2.11 on 2024-05-21 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "configuracion",
            "0015_becasmotivos_calidadintegrante_becasjugador_mesdesde_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="becasjugador",
            name="motivoSolicitud",
            field=models.ForeignKey(
                blank=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="configuracion.becasmotivos",
            ),
        ),
    ]