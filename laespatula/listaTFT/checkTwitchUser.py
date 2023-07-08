import requests
from django.shortcuts import render

from .models import jugadorTFT


def actualizaTwitch(request):
    listaFinalTFT = jugadorTFT.objects.filter(dentroLista="Si")

    body = {
        'client_id': 'mm93v8xum8ecfnjhfgxl3koi32smrx',
        'client_secret': '0vjnmox9ip7tgyfuuna2bvtmxyc2xz',
        "grant_type": 'client_credentials'
    }
    r = requests.post('https://id.twitch.tv/oauth2/token', body)

    keys = r.json()

    for i in listaFinalTFT:
        if i.twitchname != "No" and i.twitchname != '':
            checkState = checkUser(i.twitchname, keys)
            i.online = checkState
            i.save()

    context = {'listaFinalTFT1': listaFinalTFT}

    return render(request, 'oculto/actualizaTwitch.html', context)


def checkUser(userName, keys):
    API_HEADERS = {
        'Authorization': 'Bearer ' + keys['access_token'],
        'Client-ID': 'mm93v8xum8ecfnjhfgxl3koi32smrx',
    }

    url = 'https://api.twitch.tv/helix/streams?user_login=' + userName

    try:
        req = requests.Session().get(url, headers=API_HEADERS)
        jsonData = req.json()
        if len(jsonData['data']) == 1:
            state = "Online"
        else:
            state = "Offline"
    except Exception as e:
        print("Error checking user: ", e)
        state = "Offline"

    return state
