# Generated by Django 3.0.7 on 2021-03-22 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0008_jugadorrusia_ordenrank'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jugadorrusia',
            name='summonerID',
            field=models.CharField(default='No', max_length=1000),
        ),
    ]
