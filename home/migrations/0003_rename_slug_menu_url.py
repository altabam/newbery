# Generated by Django 4.2.11 on 2025-01-31 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_menu_slug'),
    ]

    operations = [
        migrations.RenameField(
            model_name='menu',
            old_name='slug',
            new_name='url',
        ),
    ]
