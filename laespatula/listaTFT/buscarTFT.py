from django.http import Http404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import jugadorTFT
from .serializers import JugadorTFTListaSerializer
import requests

api_key_tftTxt = open("listaTFT/apiKeyTFT.txt", "r")
api_key_tft = api_key_tftTxt.read()
api_key_tftTxt.close()


@api_view(['GET'])
def buscarTFT(request, jug_cuenta):
    jugadorBuscado = jugadorTFT.objects.filter(cuenta__iexact=jug_cuenta.lower())

    if not jugadorBuscado:
        raise Http404

    for jugador in jugadorBuscado:
        nombre = jugador.cuenta
        headers = {'X-Riot-Token': api_key_tft}
        U = 'https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/' + nombre
        s = requests.get(U, headers=headers)
        js = s.json()
        if s.status_code == 404:
            return Response({'error': 'El nombre de invocador ha cambiado o está almacenado de forma incorrecta'})
        else:
            jugador.summonerID = js['id']
            clave = jugador.summonerID

        URL = 'https://euw1.api.riotgames.com/tft/league/v1/entries/by-summoner/' + clave
        r = requests.get(URL, headers=headers)
        json = r.json()
        if json:
            for i in range(0, len(json)):
                if json[i]['queueType'] == 'RANKED_TFT':
                    jugador.LPs = json[i]['leaguePoints']
                    jugador.victorias = json[i]['wins']
                    jugador.derrotas = json[i]['losses']
                    jugador.tier = json[i]['tier']
                    jugador.division = json[i]['rank']
                    jugador.partidasJugadas = jugador.derrotas + jugador.victorias
                    jugador.winrate = (jugador.victorias / jugador.partidasJugadas) * 100
                    jugador.save()
        else:
            return Response({'error': 'No ha jugado suficientes partidas este Set'})

    jugadorData = JugadorTFTListaSerializer(jugador).data
    data = {'jugador': jugadorData}
    return Response(data)
