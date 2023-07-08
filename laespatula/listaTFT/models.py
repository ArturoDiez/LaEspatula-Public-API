from django.db import models


# Create your models here.
class jugadorTFT(models.Model):
    nick = models.CharField(max_length=100, blank = False, default='No')
    cuenta = models.CharField(max_length=100, blank = False, default='No')
    twitch = models.CharField(max_length=1000,default='No')
    twitter = models.CharField(max_length=1000,default='No')
    link = models.CharField(max_length=1000,default='No')
    tier = models.CharField(max_length=100,default='')
    division = models.CharField(max_length=1000,default='')
    LPs = models.IntegerField(default=0)
    summonerID = models.CharField(max_length=100,default='No')
    semana1 = models.IntegerField(default=0)
    semana2 = models.IntegerField(default=0)
    semana3 = models.IntegerField(default=0)
    semana1Fates = models.IntegerField(default=0)
    semana2Fates = models.IntegerField(default=0)
    semana3Fates = models.IntegerField(default=0)
    puntosMundialFates = models.IntegerField(default=0)
    semana1Reckoning = models.IntegerField(default=0)
    semana2Reckoning = models.IntegerField(default=0)
    semana3Reckoning = models.IntegerField(default=0)
    puntosMundialReckoning = models.IntegerField(default=0)
    partidasJugadas = models.IntegerField(default=0)
    victorias = models.IntegerField(default=0)
    derrotas = models.IntegerField(default=0)
    winrate = models.FloatField(default=0)
    picoLPs = models.IntegerField(default=0)
    topEUW = models.IntegerField(default=0)
    topESP = models.IntegerField(default=0)
    dentroLista = models.CharField(max_length=100, default='No')
    online = models.CharField(max_length=100, default='No')
    twitchname = models.CharField(max_length=1000, default='No')
    puuid = models.CharField(max_length=1000, default='No')
    ultimoGame = models.CharField(max_length=100, default='No')
    ultimaModif = models.DateTimeField(null= True)
    actualizado = models.BooleanField(default=True)

    def __str__(self):
        return self.nick


class studyDataJugadoresTFT(models.Model):
    cuenta = models.CharField(max_length=100, blank=False, default='No')
    jugadorTFT = models.ForeignKey('jugadorTFT', null=True, on_delete=models.DO_NOTHING)
    set8Data = models.JSONField(null=True)
    set8ELO = models.JSONField(null=True)
    set8BELO = models.JSONField(null=True)
    set9ELO = models.JSONField(null=True)
    streak = models.IntegerField(default=0)
    LPsParche = models.IntegerField(default=0)

    def __str__(self):
        return self.cuenta


class top1EspJugadoresTFT(models.Model):
    cuenta = models.CharField(max_length=100, blank=False, default='No')
    set = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    actual = models.BooleanField(default=False)

    def __str__(self):
        return self.cuenta

    def getDiff(self):
        if self.end_date is None:
            return None
        start, end = self.start_date, self.end_date

        if (end - start).days > 0:
            return '%s días, %s horas y %s minutos' % ((end - start).days, (end - start).seconds // 3600,
                                                       (end - start).seconds % 3600 // 60)
        if (end - start).seconds // 3600 > 0:
            return '%s horas y %s minutos' % ((end - start).seconds // 3600, (end - start).seconds % 3600 // 60)
        return '%s minutos' % ((end - start).seconds % 3600 // 60)


class top1EUJugadoresTFT(models.Model):
    cuenta = models.CharField(max_length=100, blank=False, default='No')
    set = models.FloatField(default=0)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    actual = models.BooleanField(default=False)

    def __str__(self):
        return self.cuenta

    def getDiff(self):
        if self.end_date is None:
            return None
        start, end = self.start_date, self.end_date

        if (end - start).days > 0:
            return '%s días, %s horas y %s minutos' % ((end - start).days, (end - start).seconds // 3600,
                                                       (end - start).seconds % 3600 // 60)
        if (end - start).seconds // 3600 > 0:
            return '%s horas y %s minutos' % ((end - start).seconds // 3600, (end - start).seconds % 3600 // 60)
        return '%s minutos' % ((end - start).seconds % 3600 // 60)


class jugadorEuropeoFates(models.Model):
    cuenta = models.CharField(max_length=100, blank = False, default='No')
    LPs = models.IntegerField(default=0)
    summonerID = models.CharField(max_length=100,default='No')
    semana1Fates = models.IntegerField(default=0)
    semana2Fates = models.IntegerField(default=0)
    semana3Fates = models.IntegerField(default=0)
    puntosMundial = models.IntegerField(default=0)
    diferencia = models.IntegerField(default=0)


class datosCompetitivo(models.Model):
    datos = models.JSONField()
    set = models.FloatField()
    tipo = models.CharField(null=True, max_length=100)
    region = models.CharField(max_length=30)