from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import studyDataJugadoresTFT


@api_view(['GET'])
def rivales(request, jug_cuenta):
    cuenta = jug_cuenta

    players = studyDataJugadoresTFT.objects.filter(cuenta__iexact=cuenta.lower())
    if len(players) != 0:
        for player in players:
            datos = player.set8Data

    if players:
        datosOrd = sorted(datos.items(), key=lambda a: int(a[0]), reverse=True)
        data = {'jugador': jug_cuenta, "datos": datosOrd, 'mensaje': ''}
    else:
        mensaje = jug_cuenta + ' no existe o no ha jugado partidas este set'
        data = {'jugador': jug_cuenta, "datos": [{}], 'mensaje': mensaje}

    return Response(data)


def buscaRivales(request):
    return render(request, 'tft/buscaRivales.html')
