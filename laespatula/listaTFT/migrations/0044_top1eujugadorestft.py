# Generated by Django 3.2.13 on 2022-12-25 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listaTFT', '0043_jugadortft_ultimamodif'),
    ]

    operations = [
        migrations.CreateModel(
            name='top1EUJugadoresTFT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cuenta', models.CharField(default='No', max_length=100)),
                ('set', models.FloatField(default=0)),
                ('start_date', models.DateTimeField(null=True)),
                ('end_date', models.DateTimeField(null=True)),
                ('actual', models.BooleanField(default=False)),
            ],
        ),
    ]
