# Generated by Django 3.0.7 on 2021-03-23 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0009_auto_20210322_1851'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadorrusia',
            name='partidasJugadas',
            field=models.IntegerField(default=0),
        ),
    ]
