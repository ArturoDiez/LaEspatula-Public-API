# Generated by Django 3.2.13 on 2022-06-08 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0034_auto_20220501_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydatajugadorestft',
            name='set7Data',
            field=models.JSONField(default=''),
        ),
    ]
