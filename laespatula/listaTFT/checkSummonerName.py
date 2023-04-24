import requests
import time
from django.shortcuts import render

from .models import jugadorTFT


api_key_tftTxt = open("listaTFT/apiKeyTFT.txt", "r")
api_key_tft = api_key_tftTxt.read()
api_key_tftTxt.close()


def checkSummoner(request):
    listaJugadores = jugadorTFT.objects.all()

    headers = {'X-Riot-Token': api_key_tft}

    for jugador in listaJugadores:
        time.sleep(0.2)
        if jugador.puuid == "":
            U = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + jugador.cuenta
            s = requests.get(U, headers=headers)
            js = s.json()
            jugador.puuid = js["puuid"]
            jugador.save()

        URL = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/' + jugador.puuid
        r = requests.get(URL, headers=headers)
        json = r.json()

        if json:
            if jugador.cuenta != json['name']:
                jugador.cuenta = json['name']
                jugador.link = 'https://lolchess.gg/profile/euw/' + json['name'].replace(" ", "")
                jugador.save()

    context = {'listaJugadores': listaJugadores}

    return render(request, 'oculto/actualizaSummonerName.html', context)