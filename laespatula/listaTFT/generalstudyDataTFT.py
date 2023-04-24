import plotly
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone

from .models import jugadorTFT, studyDataJugadoresTFT, top1EspJugadoresTFT
from .serializers import JugadorTFTStudyDataSerializer, JugadorTFTDataSerializer, Top1ESPSerializer
import operator
import json
from datetime import datetime, timedelta
import plotly.graph_objects as go

parchesTxt = open("listaTFT/parches.txt", "r").read()
parches = json.loads(parchesTxt)


@api_view(['GET'])
def lineData(request, setTFT):
    top1 = top1EspJugadoresTFT.objects.filter(actual=True)

    jugadores = list(jugadorTFT.objects.filter(dentroLista='Si'))

    start_date = (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
    end_date = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    jugadores.sort(key=operator.attrgetter('LPs', 'victorias'), reverse=True)
    jugadores10 = jugadores[0:10]
    players = list()
    dataToday = list()

    for jugador in jugadores10:
        playerQuery = studyDataJugadoresTFT.objects.filter(jugadorTFT=jugador)
        for player in playerQuery:
            players.append(player)

    for jugador1 in top1:
        top1Dict = Top1ESPSerializer(jugador1).data

    ahora = timezone.localtime(timezone.now())
    now = ahora.strftime('%Y-%m-%d %H:%M')

    plot_LPs = go.Figure()

    if players:
        for player in players:
            labels = []
            data = []
            league = []
            datos = player.set8BELO
            tamaño = len(datos)

            for i in range(0, tamaño):
                j = str(i)
                labels.append(datos[j]['datetime'])
                data.append(datos[j]['LP'])
                league.append(datos[j]['liga'])

            labels.append(now)
            for jugador in jugadores10:
                if jugador.cuenta == player.cuenta:
                    data.append(jugador.LPs)
                    dataToday.append(jugador.LPs)
                    league.append(jugador.tier)

            plot_LPs.add_trace(go.Scatter(name=player.cuenta, x=labels, y=data,
                                          mode='lines+markers', marker=dict(size=10)))

        plot_LPs.update_xaxes(range=[start_date, end_date])

        plot_LPs.update_yaxes(range=[min(dataToday) - 100, max(dataToday) + 100])

        plot_LPs.update_layout(title=dict(text='Top español', font=dict(size=25)),
                               title_font_color='#FFFF66',
                               xaxis=dict(
                                   title='Fecha'),
                               yaxis=dict(
                                   title='LPs',
                                   rangemode='nonnegative'),
                               font_color='#FFFF66',
                               plot_bgcolor='lightblue',
                               paper_bgcolor='rgba(0,0,0,0)')

    plot = plotly.io.to_json(plot_LPs)

    data = {'top1': top1Dict, 'plot': plot}

    return Response(data)


@api_view(['GET'])
def top1Esp(request, setTFT):
    listaTop = top1EspJugadoresTFT.objects.filter(set=float(setTFT)).order_by('-start_date')

    data = Top1ESPSerializer(listaTop, many=True).data
    return Response(data)


@api_view(['GET'])
def masVictList(request, numero):
    jugadores = jugadorTFT.objects.filter(dentroLista='Si').order_by('-victorias')
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTDataSerializer(jugadores, many=True, fields=('cuenta', 'victorias')).data

    return Response(data)


@api_view(['GET'])
def masWRList(request, numero):
    jugadores = jugadorTFT.objects.filter(dentroLista='Si').order_by('-winrate')
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTDataSerializer(jugadores, many=True, fields=('cuenta', 'winrate')).data

    return Response(data)


@api_view(['GET'])
def masVicioList(request, numero):
    jugadores = jugadorTFT.objects.filter(dentroLista='Si').order_by('-partidasJugadas')
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTDataSerializer(jugadores, many=True, fields=('cuenta', 'partidasJugadas')).data

    return Response(data)


@api_view(['GET'])
def hottestStreakList(request, numero):
    jugadores = list(
        studyDataJugadoresTFT.objects.filter(jugadorTFT__dentroLista='Si').filter(streak__gt=0).order_by('-streak'))
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTStudyDataSerializer(jugadores, many=True, fields=('cuenta', 'streak')).data

    return Response(data)


@api_view(['GET'])
def coldestStreakList(request, numero):
    jugadores = list(
        studyDataJugadoresTFT.objects.filter(jugadorTFT__dentroLista='Si').filter(streak__lt=0).order_by('streak'))
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTStudyDataSerializer(jugadores, many=True, fields=('cuenta', 'streak')).data

    return Response(data)


@api_view(['GET'])
def rachaMasList(request, numero):
    jugadores = list(
        studyDataJugadoresTFT.objects.filter(jugadorTFT__dentroLista='Si').filter(LPsParche__gt=0).order_by(
            '-LPsParche'))
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTStudyDataSerializer(jugadores, many=True,
                                         fields=('cuenta', 'LPsParche')).data

    return Response(data)


@api_view(['GET'])
def rachaMenosList(request, numero):
    jugadores = list(
        studyDataJugadoresTFT.objects.filter(jugadorTFT__dentroLista='Si').filter(LPsParche__lt=0).order_by(
            'LPsParche'))
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTStudyDataSerializer(jugadores, many=True,
                                         fields=('cuenta', 'LPsParche')).data

    return Response(data)


@api_view(['GET'])
def picosLPsList(request, numero):
    jugadores = list(jugadorTFT.objects.filter(dentroLista="Si").order_by('-picoLPs'))
    if numero == '5':
        jugadores = jugadores[0:5]
    data = JugadorTFTDataSerializer(jugadores, many=True, fields=('cuenta', 'picoLPs')).data

    return Response(data)


def actualizaDatos(request):
    jugadores = list(jugadorTFT.objects.filter(dentroLista='Si'))

    for jugador in jugadores:
        playerQuery = studyDataJugadoresTFT.objects.filter(cuenta=jugador.cuenta)
        for player in playerQuery:
            datos = player.set8BELO
            if datos is not None:
                tamaño = len(datos)
            else:
                tamaño = 0
            if tamaño > 2:
                if datos[str(tamaño - 1)]['LP'] > datos[str(tamaño - 2)]['LP']:
                    player.streak = hottestStreaks(player)
                    player.save()
                else:
                    player.streak = coldestStreaks(player)
                    player.save()
                racha = rachaParche(player)
                if racha >= 0:
                    player.LPsParche = racha
                    player.save()
                else:
                    player.LPsParche = racha
                    player.save()
                pico = picoLPs(player)
                if pico > jugador.picoLPs:
                    jugador.picoLPs = pico
                    jugador.save()

    return render(request, 'oculto/actualizaDatos.html')


def masWinrate(listaJugadores):
    masWR = listaJugadores
    masWR.sort(key=operator.attrgetter('winrate'), reverse=True)
    return masWR


def masVict(listaJugadores):
    masVictorias = listaJugadores
    masVictorias.sort(key=operator.attrgetter('victorias'), reverse=True)
    return masVictorias


def masVicio(listaJugadores):
    masVicio = listaJugadores
    masVicio.sort(key=operator.attrgetter('partidasJugadas'), reverse=True)
    return masVicio


def hottestStreaks(player):
    hotStreak = 0
    datos = player.set8BELO
    tamaño = len(datos)
    LPantes = datos['0']['LP']

    for i in range(1, tamaño):
        j = str(i)
        LP = datos[j]['LP']
        diff = LP - LPantes
        if diff > 0:
            hotStreak += diff
        else:
            hotStreak = 0
        LPantes = LP

    return hotStreak


def coldestStreaks(player):
    coldStreak = 0
    datos = player.set8BELO
    tamaño = len(datos)
    LPantes = datos['0']['LP']

    for i in range(1, tamaño):
        j = str(i)
        LP = datos[j]['LP']
        diff = -(LP - LPantes)
        if diff > 0:
            coldStreak += diff
        else:
            coldStreak = 0
        LPantes = LP

    return coldStreak


def rachaParche(player):
    ahora = timezone.localtime(timezone.now())
    dateTime = ahora.strftime('%Y-%m-%d %H:%M')
    ultimoParche = "2022-01-01"
    datos = player.set8BELO
    tamaño = len(datos)

    LPinicial = 0
    haJugado = False
    streak = 0

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
    datos = player.set8BELO
    if datos is None:
        tamaño = 0
    else:
        tamaño = len(datos)

    for i in range(1, tamaño):
        j = str(i)
        if datos[j]['LP'] > pico:
            pico = datos[j]['LP']

    return pico
