# Generated by Django 3.2.13 on 2022-12-23 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0042_auto_20221207_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadortft',
            name='ultimaModif',
            field=models.DateTimeField(null=True),
        ),
    ]
