# Generated by Django 3.0.7 on 2021-06-14 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0010_jugadorrusia_partidasjugadas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jugadortft',
            old_name='puntosMundial',
            new_name='puntosMundialFates',
        ),
    ]
