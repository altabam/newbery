# Generated by Django 4.2.11 on 2024-05-12 20:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('configuracion', '0010_rename_personas_socios_persona'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cuota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('concepto', models.CharField(max_length=100)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=9)),
                ('cant_hermanos', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='socios',
            name='fecha_alta',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='socios',
            name='fecha_baja',
            field=models.DateField(null=True),
        ),
    ]
