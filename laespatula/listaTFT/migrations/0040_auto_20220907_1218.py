# Generated by Django 3.2.13 on 2022-09-07 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0039_datoscompetitivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydatajugadorestft',
            name='set7BData',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='studydatajugadorestft',
            name='set7BELO',
            field=models.JSONField(default={}),
        ),
    ]