# Generated by Django 3.0.7 on 2021-09-13 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0016_jugadortft_dentrolista'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadorlor',
            name='dentroLista',
            field=models.CharField(default='No', max_length=100),
        ),
    ]
