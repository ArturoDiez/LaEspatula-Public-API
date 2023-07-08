from django.utils import timezone
from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import jugadorTFT, studyDataJugadoresTFT
from .serializers import JugadorTFTListaSerializer
from datetime import datetime, timedelta
import json

api_key_tftTxt = open("listaTFT/apiKeyTFT.txt", "r")
api_key_tft = api_key_tftTxt.read()
api_key_tftTxt.close()

parchesTxt = open("listaTFT/parches.txt", "r").read()
parches = json.loads(parchesTxt)


@api_view(['GET'])
def lineData(request, jug_cuenta):
    # Declaración de listas
    labels = []
    data = []
    league = []

    # Declaración de constantes
    hotStreak = 0
    hottestStreak = 0
    coldStreak = 0
    coldestStreak = 0
    rachaP = 0
    pico = 0
    posMed = 0
    tamaño = 0

    jugador = jugadorTFT.objects.filter(cuenta__iexact=jug_cuenta.lower())
    dataJug = JugadorTFTListaSerializer(jugador, many=True).data

    start_date = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
    print(start_date)

    for j in jugador:
        players = studyDataJugadoresTFT.objects.filter(jugadorTFT=j)

    if not jugador:
        raise Http404

    if len(players) != 0:
        for player in players:
            datos = player.set9ELO
            if datos != {} and datos is not None:
                hottestStreak, hotStreak = hottestStreaks(player)
                coldestStreak, coldStreak = coldestStreaks(player)
                rachaP = rachaParche(player)
                pico = picoLPs(player)
                tamaño = len(datos)

            for i in range(0, tamaño):
                j = str(i)
                print(datos[j]['datetime'])
                if start_date > datos[j]['datetime']:
                    continue
                labels.append(datos[j]['datetime'])
                data.append(datos[j]['LP'])
                league.append(datos[j]['liga'])

                #posMed = posMedia(player, tamaño)

    data = {'jugador': dataJug, 'labels': labels, 'elo': data, 'league': league,
            'rachaP': rachaP, 'pico': pico,
            'tamaño': tamaño, 'hotStreak': hotStreak, 'hottestStreak': hottestStreak,
            'coldStreak': coldStreak, 'coldestStreak': coldestStreak}

    return Response(data)


def hottestStreaks(player):
    hottestStreak = 0
    hotStreak = 0
    datos = player.set9ELO
    if datos is not None:
        tamaño = len(datos)
        LPantes = datos['0']['LP']
    else:
        return hottestStreak, hotStreak

    for i in range(1, tamaño):
        j = str(i)

        LP = datos[j]['LP']
        diff = LP - LPantes
        if diff > 0:
            hotStreak += diff
            if hotStreak > hottestStreak:
                hottestStreak = hotStreak
        else:
            hotStreak = 0
        LPantes = LP

    return hottestStreak, hotStreak


def coldestStreaks(player):
    coldestStreak = 0
    coldStreak = 0
    datos = player.set9ELO
    if datos is not None:
        tamaño = len(datos)
        LPantes = datos['0']['LP']
    else:
        return coldestStreak, coldStreak

    for i in range(1, tamaño):
        j = str(i)
        LP = datos[j]['LP']
        diff = LP - LPantes
        if diff < 0:
            coldStreak += diff
            if coldStreak < coldestStreak:
                coldestStreak = coldStreak
        else:
            coldStreak = 0
        LPantes = LP

    return coldestStreak, coldStreak


def rachaParche(player):
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')
    ultimoParche = "2022-01-01"
    LPinicial = 0
    haJugado = False
    streak = 0
    datos = player.set9ELO
    if datos is not None:
        tamaño = len(datos)
    else:
        return streak

    for i in list(parches.items()):
        if i[1] > dateTime:
            break
        ultimoParche = i[1]

    for i in range(1, tamaño):
        j = str(i)
        if datos[j]['datetime'] >= ultimoParche:
            LPinicial = datos[j]['LP']
            haJugado = True

            break
    if haJugado:
        streak = datos[str(tamaño - 1)]['LP'] - LPinicial

    return streak


def picoLPs(player):
    pico = 0
    datos = player.set9ELO
    if datos is not None:
        tamaño = len(datos)
    else:
        return pico

    for i in range(1, tamaño):
        j = str(i)
        if datos[j]['LP'] > pico:
            pico = datos[j]['LP']

    return pico


def posMedia(player, tamaño):
    media = 0
    placements = list()
    datos = player.set9ELO
    if datos is not None:
        tdatos = len(datos)
    else:
        return 0

    size = tamaño
    if tamaño >= 10:
        size = 10

    if len(datos) == 0:
        return 0

    for partido in range(0, size):
        posicion = datos[str(tdatos - 1 - partido)]['placement']
        placements.append(posicion)

    for place in placements:
        media += place

    posMed = media / size

    return posMed
