from django.shortcuts import render
from django.db import connection

# Create your views here.
def actualizarSecuenciaIdPersonas(request):
    with connection.cursor() as cursor:
      cursor.execute("SELECT setval(pg_get_serial_sequence('""configuracion_personas""','id'), coalesce(max('id'), 1), max('id') IS NOT null) FROM 'configuracion_personas';")
    return render(request,'configuracion/cargaMasiva.html', contexto)   