from django.shortcuts import render
from .models import jugadorTFT, studyDataJugadoresTFT
import requests
import json
import time
from django.utils import timezone

api_key_tftTxt = open("listaTFT/apiKeyTFT.txt", "r")
api_key_tft = api_key_tftTxt.read()
api_key_tftTxt.close()


def actualizaPartidos(request):
    headers = {'X-Riot-Token': api_key_tft}
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')
    listaJugadores = jugadorTFT.objects.all()

    dataJugadores = studyDataJugadoresTFT.objects.all()
    listDataJugadores = list()
    listCuentaDataJugadores = list()

    for j in dataJugadores:
        listDataJugadores.append(j)
        listCuentaDataJugadores.append(j.cuenta)

    for jugador in listaJugadores:
        time.sleep(0.2)
        LP = jugador.LPs
        ligaJug = jugador.tier

        if jugador.puuid == "":
            U = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + jugador.cuenta
            s = requests.get(U, headers=headers)
            js = s.json()
            jugador.puuid = js["puuid"]
            jugador.save()
        puuid = jugador.puuid
        placement = 0
        partido = ''
        rivales = {}
        rival = 1
        averLPs = 0

        url = 'https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/' + puuid + '/ids?start=0&count=1'
        reponse = requests.get(url, headers=headers)
        partidos = reponse.json()

        for part in partidos:
            partido = part

        if jugador.ultimoGame == partido:
            continue

        url2 = 'https://europe.api.riotgames.com/tft/match/v1/matches/' + partido
        reponse2 = requests.get(url2, headers=headers)
        datos = reponse2.json()

        if reponse2.status_code == 403 or reponse2.status_code == 404:
            continue

        #version = datos['info']['game_version']
        #num_version = 0
        #if version[12:13] == '.':
        #    num_version = int(version[11:12])
        #else:
        #    num_version = int(version[11:13])

        #if num_version < 17:
        #    jugador.ultimoGame = partido
        #    jugador.actualizado = False
        #    continue

        for participant in datos['info']['participants']:
            if participant['puuid'] == puuid:
                placement = participant['placement']
            else:
                url3 = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + participant['puuid']
                reponse3 = requests.get(url3, headers=headers)
                datosLeagueP = reponse3.json()
                url4 = 'https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/' + datosLeagueP['id']
                reponse4 = requests.get(url4, headers=headers)
                datosPlayer = reponse4.json()
                for i in range(0, len(datosPlayer)):
                    if datosPlayer[i]['queueType'] == 'RANKED_TFT':
                        cuenta = datosPlayer[i]['summonerName']
                        LPs = datosPlayer[i]['leaguePoints']
                        liga = datosPlayer[i]['tier']
                        placementRival = participant['placement']
                        rivales[rival] = {
                            "cuenta": cuenta,
                            "liga": liga,
                            "LPs": LPs,
                            "placementRival": placementRival
                        }
                        if liga == "MASTER" or liga == "GRANDMASTER" or liga == "CHALLENGER":
                            averLPs += LPs
                        else:
                            averLPs += 0
                        rival += 1

        averLPs = averLPs / 7
        tipoPartida = datos['info']['queue_id']

        infoAdded = {"datetime": dateTime,
                     "LP": LP,
                     "liga": ligaJug,
                     "placement": placement,
                     "rivales": rivales,
                     "mediaLPs": averLPs,
                     "tipo de partida": tipoPartida
                     }

        if jugador.cuenta not in listCuentaDataJugadores:
            data = {"0":
                        {"datetime": dateTime,
                         "LP": LP,
                         "liga": ligaJug,
                         "placement": placement,
                         "rivales": rivales,
                         "mediaLPs": averLPs,
                         "tipo de partida": tipoPartida
                         }
                    }

            json.dumps(data)

            jugadorStudied = studyDataJugadoresTFT(cuenta=jugador.cuenta, set8Data=data)
            jugadorStudied.save()
            jugador.ultimoGame = partido
            jugador.actualizado = True
            jugador.save()

        else:
            for dataJugador in listDataJugadores:
                if jugador.cuenta == dataJugador.cuenta:
                    data = dataJugador.set8Data
                    if data is not None:
                        jsonSize = len(data)
                        data[jsonSize] = infoAdded
                    else:
                        data = {"0":
                                    {"datetime": dateTime,
                                     "LP": LP,
                                     "liga": ligaJug,
                                     "placement": placement,
                                     "rivales": rivales,
                                     "mediaLPs": averLPs,
                                     "tipo de partida": tipoPartida
                                     }
                                }
                        json.dumps(data)

                    dataJugador.set8Data = data
                    dataJugador.save()

                    jugador.ultimoGame = partido
                    jugador.actualizado = True
                    jugador.save()

    return render(request, 'oculto/actualizaPartidos.html')
