# Generated by Django 3.2.13 on 2022-06-12 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0037_remove_studydatajugadorestft_set7data'),
    ]

    operations = [
        migrations.AddField(
            model_name='studydatajugadorestft',
            name='set7Data',
            field=models.JSONField(default={}),
        ),
    ]
