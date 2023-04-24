from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import datosCompetitivo


@api_view(['GET'])
def snapshotsESP(request, setTFT, numeroSnapshot):
    snapRaw = datosCompetitivo.objects.get(tipo=numeroSnapshot, set=setTFT, region="ESP")
    data = {"numeroSnapshot": numeroSnapshot, 'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def snapshotsEU(request, setTFT, numeroSnapshot):
    snapRaw = datosCompetitivo.objects.get(tipo=numeroSnapshot, set=setTFT, region="EU")
    data = {"numeroSnapshot": numeroSnapshot, 'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def cupsESP(request, setTFT, numeroCopa):
    snapRaw = datosCompetitivo.objects.get(tipo=numeroCopa, set=setTFT, region="ESP")
    data = {"numeroSnapshot": numeroCopa, 'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def GSCEU(request, setTFT, numeroGSC):
    snapRaw = datosCompetitivo.objects.get(tipo=numeroGSC, set=setTFT, region="EU")
    data = {"numeroSnapshot": numeroGSC, 'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def totalESP(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total", set=setTFT, region="ESP")
    data = {'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def totalSnapESP(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total Snapshot", set=setTFT, region="ESP")
    data = {'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def totalCupsESP(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total Cups", set=setTFT, region="ESP")
    data = {'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def totalSnapEU(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total Snapshot", set=setTFT, region="EU")
    data = {'datos': snapRaw.datos}

    return Response(data)


# TODO Hay que cambiar esto una vez esté en funcionamiento
@api_view(['GET'])
def totalSnapEU2(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total Snapshot2", set=setTFT, region="EU")
    data = {'datos': snapRaw.datos}

    return Response(data)


@api_view(['GET'])
def totalGSCEU(request, setTFT):
    snapRaw = datosCompetitivo.objects.get(tipo="Total GSCs", set=setTFT, region="EU")
    data = {'datos': snapRaw.datos}

    return Response(data)
