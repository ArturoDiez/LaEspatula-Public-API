from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.utils import timezone

from .models import jugadorTFT, studyDataJugadoresTFT, top1EspJugadoresTFT, datosCompetitivo, top1EUJugadoresTFT
from .serializers import JugadorTFTListaSerializer

import requests
import json
import operator


api_key_tftTxt = open("listaTFT/apiKeyTFT.txt", "r")
api_key_tft = api_key_tftTxt.read()
api_key_tftTxt.close()


def actualizaTFT(request):
    # Tomar valores de Ch y GM, comparar con base de datos y sacar los que estén
    headers = {'X-Riot-Token': api_key_tft}
    URLChallenger = 'https://euw1.api.riotgames.com/tft/league/v1/challenger'
    ch = requests.get(URLChallenger, headers=headers)
    Challengers = ch.json()
    ChallengersOrdered = sorted(Challengers['entries'], key=lambda x: x["leaguePoints"], reverse=True)

    URLGrandMasters = 'https://euw1.api.riotgames.com/tft/league/v1/grandmaster'
    gm = requests.get(URLGrandMasters, headers=headers)
    GrandMasters = gm.json()
    GrandMastersOrdered = sorted(GrandMasters['entries'], key=lambda x: x["leaguePoints"], reverse=True)

    URLMasters = 'https://euw1.api.riotgames.com/tft/league/v1/master'
    m = requests.get(URLMasters, headers=headers)
    Masters = m.json()
    MastersOrdered = sorted(Masters['entries'], key=lambda x: x["leaguePoints"], reverse=True)

    listaJugadoresYaDentro = jugadorTFT.objects.filter(dentroLista="Si")
    listaJugadoresFuera = list()
    listaJugadoresDentro = list()

    for j in listaJugadoresYaDentro:
        listaJugadoresFuera.append(j)

    listaChallengerSize = len(Challengers['entries'])
    listaGMasterSize = len(GrandMasters['entries'])
    listaMasterSize = len(Masters['entries'])

    listaJugadoresFuera, listaJugadoresDentro = actualizarCambiosPorLista('Challenger', ChallengersOrdered,
                                                                          listaJugadoresFuera, listaJugadoresDentro,
                                                                          listaChallengerSize, 0, 0, headers)
    listaJugadoresFuera, listaJugadoresDentro = actualizarCambiosPorLista('GrandMaster', GrandMastersOrdered,
                                                                          listaJugadoresFuera, listaJugadoresDentro,
                                                                          listaGMasterSize, listaChallengerSize, 0,
                                                                          headers)
    listaJugadoresFuera, listaJugadoresDentro = actualizarCambiosPorLista('Master', MastersOrdered, listaJugadoresFuera,
                                                                          listaJugadoresDentro, listaMasterSize,
                                                                          listaChallengerSize, listaGMasterSize,
                                                                          headers)

    for j in listaJugadoresFuera:
        if j.dentroLista != 'No':
            j.dentroLista = 'No'
            j.save()

    listaJugadores = list(jugadorTFT.objects.filter(dentroLista="Si").order_by("-LPs", "topEUW"))
    for jugador in listaJugadores:
        jugador.topESP = listaJugadores.index(jugador) + 1
        jugador.save()

    ChList = datosCompetitivo.objects.get(tipo="Challenger")
    ChList.datos = ChallengersOrdered
    ChList.save()

    GMList = datosCompetitivo.objects.get(tipo="GrandMaster")
    GMList.datos = GrandMastersOrdered
    GMList.save()

    MList = datosCompetitivo.objects.get(tipo="Master")
    MList.datos = MastersOrdered
    MList.save()

    storeELO(listaJugadoresDentro)
    top1EspAct()
    top1EUAct()

    return render(request, 'oculto/actualizaTFT.html')


def actualizarCambiosPorLista(tipoLista, lista, listaJugadoresFuera, listaJugadoresDentro,
                              listaSize, listaSizeCH, listaSizeGM, headers):
    listaJugadoresTFT = jugadorTFT.objects.all()

    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')

    for j in listaJugadoresTFT:
        for i in range(0, listaSize):
            if j.cuenta == lista[i]['summonerName']:
                jugador = jugadorTFT.objects.get(cuenta=lista[i]['summonerName'])
                if j not in listaJugadoresFuera:
                    if j.summonerID == "":
                        U = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + jugador.cuenta
                        s = requests.get(U, headers=headers)
                        js = s.json()
                        jugador.summonerID = js["id"]
                        jugador.save()

                    if jugador.summonerID != lista[i]['summonerId']:
                        continue
                else:
                    listaJugadoresFuera.remove(j)

                LPsAntiguos = jugador.LPs

                if (listaSizeCH + listaSizeGM + i + 1) != jugador.topEUW:
                    jugador.topEUW = listaSizeCH + listaSizeGM + i + 1
                    jugador.save()

                if LPsAntiguos == lista[i]['leaguePoints'] and jugador.tier == tipoLista:
                    continue

                jugador.LPs = lista[i]['leaguePoints']
                jugador.victorias = lista[i]['wins']
                jugador.derrotas = lista[i]['losses']
                jugador.tier = tipoLista
                jugador.partidasJugadas = jugador.derrotas + jugador.victorias
                jugador.winrate = (jugador.victorias / jugador.partidasJugadas) * 100
                jugador.topEUW = listaSizeCH + listaSizeGM + i + 1
                jugador.dentroLista = 'Si'
                jugador.ultimaModif = dateTime

                jugador.save()
                listaJugadoresDentro.append(jugador)

    return listaJugadoresFuera, listaJugadoresDentro


@api_view(["GET"])
def listaTFT(request):
    listaJugadores = jugadorTFT.objects.filter(dentroLista="Si")

    listaFinalTFT = list()

    for j in listaJugadores:
        listaFinalTFT.append(j)

    listaFinalTFT.sort(key=operator.attrgetter('topESP'))
    listaFinalTFTSorted = listaFinalTFT[0:100]

    data = JugadorTFTListaSerializer(listaFinalTFTSorted, many=True).data

    return Response(data)


@api_view(["GET"])
def listaTFTonline(request):
    listaJugadores = jugadorTFT.objects.filter(online="Online")

    listaFinalTFT = list()

    for j in listaJugadores:
        listaFinalTFT.append(j)

    listaFinalTFT.sort(key=operator.attrgetter('topESP'))
    listaFinalTFTSorted = listaFinalTFT[0:100]

    data = JugadorTFTListaSerializer(listaFinalTFTSorted, many=True).data

    return Response(data)


def top1EspAct() -> None:
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')

    listaTop = list(top1EspJugadoresTFT.objects.filter(actual=True))
    listaTFTTop1 = list(jugadorTFT.objects.filter(dentroLista="Si"))

    listaTFTTop1.sort(key=operator.attrgetter('LPs', 'victorias'), reverse=True)

    for top in listaTop:
        if top.cuenta == listaTFTTop1[0].cuenta:
            break
        if top:
            top.end_date = dateTime
            top.actual = False
            top.save()
            nuevoTop = top1EspJugadoresTFT()
            nuevoTop.cuenta = listaTFTTop1[0].cuenta
            nuevoTop.start_date = dateTime
            nuevoTop.actual = True
            nuevoTop.set = 8.5
            nuevoTop.save()


def top1EUAct() -> None:
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')

    listaChallenger = datosCompetitivo.objects.get(tipo="Challenger")
    listaTop = list(top1EUJugadoresTFT.objects.filter(actual=True))

    for top in listaTop:
        if top.cuenta == listaChallenger.datos[0]['summonerName']:
            break
        else:
            if top:
                top.end_date = dateTime
                top.actual = False
                top.save()
        nuevoTop = top1EUJugadoresTFT()
        nuevoTop.cuenta = listaChallenger.datos[0]['summonerName']
        nuevoTop.start_date = dateTime
        nuevoTop.actual = True
        nuevoTop.set = 8.5
        nuevoTop.save()


def storeELO(listaJugadores) -> None:
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')

    dataJugadores = studyDataJugadoresTFT.objects.all()
    listDataJugadores = list()
    listCuentaDataJugadores = list()

    for j in dataJugadores:
        listDataJugadores.append(j)
        listCuentaDataJugadores.append(j.jugadorTFT)

    for jugador in listaJugadores:
        LP = jugador.LPs
        liga = jugador.tier

        infoAdded = {"datetime": dateTime,
                     "LP": LP,
                     "liga": liga,
                     }
        if jugador not in listCuentaDataJugadores:
            data = {"0":
                        {"datetime": dateTime,
                         "LP": LP,
                         "liga": liga,
                         }
                    }

            json.dumps(data)

            jugadorStudied = studyDataJugadoresTFT(cuenta=jugador.cuenta, set8BELO=data, jugadorTFT=jugador)
            jugadorStudied.save()
        else:
            for dataJugador in listDataJugadores:
                if jugador == dataJugador.jugadorTFT:
                    data = dataJugador.set8BELO

                    if data is not None:
                        lastValue = len(data) - 1
                        if data[str(lastValue)]['LP'] == LP and data[str(lastValue)]['liga'] == liga:
                            continue
                        jsonSize = len(data)
                        data[jsonSize] = infoAdded
                    else:
                        data = {"0":
                                    {"datetime": dateTime,
                                     "LP": LP,
                                     "liga": liga,
                                     }
                                }
                        json.dumps(data)

                    dataJugador.set8BELO = data
                    if dataJugador.cuenta != jugador.cuenta:
                        dataJugador.cuenta = jugador.cuenta
                    dataJugador.save()
