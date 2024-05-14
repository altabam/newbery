# Generated by Django 4.2.11 on 2024-05-12 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('configuracion', '0011_cuota_socios_fecha_alta_socios_fecha_baja'),
        ('cobros', '0004_delete_cobros'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_pago', models.DateField()),
                ('monto', models.FloatField()),
                ('socio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='configuracion.socios')),
            ],
        ),
        migrations.CreateModel(
            name='DetallePagos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anio', models.CharField(max_length=4)),
                ('mes', models.CharField(blank=True, choices=[('ENE', 'Enero'), ('FEB', 'Febrero'), ('MAR', 'Marzo'), ('ABR', 'Abril'), ('MAY', 'Mayo'), ('JUN', 'Junio'), ('JUL', 'Julio'), ('AGO', 'Agosto'), ('SEP', 'Septiembre'), ('OCT', 'Octubre'), ('NOV', 'Noviembre'), ('DIC', 'Diciembre')], max_length=3)),
                ('pago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cobros.pagos')),
            ],
        ),
    ]