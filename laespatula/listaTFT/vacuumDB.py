from django.db import connections
from django.shortcuts import render


def vacuum_db(request):
    with connections['default'].cursor() as cursor:
        cursor.execute("VACUUM FULL")
    return render(request, 'oculto/vacuumDB.html')
