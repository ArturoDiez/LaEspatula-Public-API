# Generated by Django 3.0.7 on 2021-03-22 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0007_equipolatam'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadorrusia',
            name='ordenrank',
            field=models.IntegerField(default=0),
        ),
    ]
