from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import jugadorTFT, jugadorEuropeoFates
from .serializers import JugadorTFTListaSerializer, dataFatesEUWSerializer


@api_view(["GET"])
def listaTFTdataFates(request):
    listaJugadores = jugadorTFT.objects.filter(puntosMundialFates__gt=0).order_by('-puntosMundialFates')

    data = JugadorTFTListaSerializer(listaJugadores, many=True).data

    return Response(data)


@api_view(["GET"])
def listaTFTdataReckoning(request):
    listaJugadores = jugadorTFT.objects.filter(puntosMundialReckoning__gt=0).order_by('-puntosMundialReckoning')

    data = JugadorTFTListaSerializer(listaJugadores, many=True).data

    return Response(data)


@api_view(["GET"])
def listaTFTdataFatesEU(request):
    listaJugadores = jugadorEuropeoFates.objects.all().order_by('-puntosMundial')

    data = dataFatesEUWSerializer(listaJugadores, many=True).data

    return Response(data)
