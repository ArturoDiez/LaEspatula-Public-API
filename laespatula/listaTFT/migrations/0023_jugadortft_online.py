# Generated by Django 3.2.12 on 2022-04-16 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0022_studydatajugadorestft'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugadortft',
            name='online',
            field=models.CharField(default='No', max_length=100),
        ),
    ]