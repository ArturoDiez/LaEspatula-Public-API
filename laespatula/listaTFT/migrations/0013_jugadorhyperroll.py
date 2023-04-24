# Generated by Django 3.0.7 on 2021-06-14 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0012_auto_20210614_1650'),
    ]

    operations = [
        migrations.CreateModel(
            name='jugadorHyperroll',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=100)),
                ('cuenta', models.CharField(default='No', max_length=100)),
                ('twitch', models.CharField(default='No', max_length=1000)),
                ('twitter', models.CharField(default='No', max_length=1000)),
                ('link', models.CharField(default='No', max_length=1000)),
                ('tier', models.CharField(default='', max_length=100)),
                ('LPs', models.IntegerField(default=0)),
                ('summonerID', models.CharField(default='No', max_length=1000)),
                ('victorias', models.IntegerField(default=0)),
                ('derrotas', models.IntegerField(default=0)),
                ('partidasJugadas', models.IntegerField(default=0)),
                ('winrate', models.FloatField(default=0)),
            ],
        ),
    ]