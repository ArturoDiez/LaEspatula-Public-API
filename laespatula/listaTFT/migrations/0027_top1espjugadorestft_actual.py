# Generated by Django 3.2.13 on 2022-04-21 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0026_top1espjugadorestft'),
    ]

    operations = [
        migrations.AddField(
            model_name='top1espjugadorestft',
            name='actual',
            field=models.BooleanField(default=False),
        ),
    ]
