from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import datosCompetitivo, top1EUJugadoresTFT
from .serializers import Top1EUWSerializer, datosCompetitivoSerializer


@api_view(['GET'])
def listaTFTEU(request, liga):
    puesto = 26
    Challenger = datosCompetitivo.objects.get(tipo="Challenger")
    GrandMaster = datosCompetitivo.objects.get(tipo="GrandMaster")
    Master = datosCompetitivo.objects.get(tipo="Master")

    top26 = 0
    if len(Challenger.datos) > 26:
        top26 = Challenger.datos[int(puesto) - 1]["leaguePoints"]
    else:
        top26 = Challenger.datos[-1]["leaguePoints"]
    corteCh = 0
    corteGM = 0

    if liga is None:
        liga = "Challenger"
    listaF = datosCompetitivo.objects.get(tipo=liga)

    if len(Challenger.datos) > 10:
        LastChallengers = lastElements(Challenger)
        LastGM = firstElements(GrandMaster)
        for i in range(0, 9):
            if LastGM[i] > LastChallengers[i]:
                corteCh = LastGM[i]
            else:
                if LastChallengers[i] < corteCh or corteCh == 0:
                    corteCh = LastChallengers[i]
                break

    if len(GrandMaster.datos) > 10:
        LastGM2 = lastElements(GrandMaster)
        LastM = firstElements(Master)
        for i in range(0, 9):
            if LastM[i] > LastGM2[i]:
                corteGM = LastM[i]
            else:
                if LastGM2[i] < corteCh or corteGM == 0:
                    corteGM = LastGM2[i]
                break

    listaFinal = datosCompetitivoSerializer(listaF).data
    data = {"top26": top26, "corteCh": corteCh, "corteGM": corteGM, "liga": liga,
            "puesto": puesto, "lista": listaFinal}
    return Response(data)


@api_view(['GET'])
def top1EU(request, setTFT):
    listaTop = top1EUJugadoresTFT.objects.filter(set=float(setTFT)).order_by('-start_date')

    data = Top1EUWSerializer(listaTop, many=True).data

    return Response(data)


def lastElements(listEntera):
    lista = list()

    for i in range(1, 10):
        LP = listEntera.datos[-i]["leaguePoints"]
        lista.append(LP)

    return lista


def firstElements(listEntera):
    lista = list()

    for i in range(0, 9):
        LP = listEntera.datos[i]["leaguePoints"]
        lista.append(LP)

    return lista
