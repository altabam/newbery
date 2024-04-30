from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
from  configuracion.models import Socios

# Create your views here.

def render_cobros(request):
    
    return render(request, "cobros.html", )
    
def busqueda_socio(request):
     if request.method == 'GET':
        socio = Socios.objects.filter(numero__startswith= request.GET['apellido'] )
        personas ="encontrado"
        return  HttpResponse( json.dumps( list(personas)), content_type='application/json' ) 
     else:
         return HttpResponse("Solo Ajax")
