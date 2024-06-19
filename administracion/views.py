from django.shortcuts import render
from django.db import connection

# Create your views here.
def actualizarSecuenciaIdPersonas(request):
    with connection.cursor() as cursor:
      cursor.execute("SELECT SETVAL((SELECT PG_GET_SERIAL_SEQUENCE('configuracion_personas', 'id')), (SELECT (MAX('id') + 1) FROM 'configuracion_personas'), FALSE);")
    return render(request,'configuracion/cargaMasiva.html', contexto)   