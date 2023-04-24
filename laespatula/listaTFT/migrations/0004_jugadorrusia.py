# Generated by Django 3.0.7 on 2021-03-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0003_auto_20210222_1425'),
    ]

    operations = [
        migrations.CreateModel(
            name='jugadorRusia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nick', models.CharField(max_length=100)),
                ('cuenta', models.CharField(default='No', max_length=100)),
                ('twitch', models.CharField(default='No', max_length=1000)),
                ('twitter', models.CharField(default='No', max_length=1000)),
                ('link', models.CharField(default='No', max_length=1000)),
                ('twitchname', models.CharField(default='No', max_length=1000)),
                ('online', models.CharField(default='No', max_length=1000)),
                ('idtwitch', models.IntegerField(default=0)),
                ('tier', models.CharField(default='', max_length=100)),
                ('division', models.CharField(default='', max_length=1000)),
                ('LPs', models.IntegerField(default=0)),
                ('summonerID', models.CharField(default='No', max_length=100)),
                ('victorias', models.IntegerField(default=0)),
                ('derrotas', models.IntegerField(default=0)),
                ('winrate', models.FloatField(default=0)),
            ],
        ),
    ]
