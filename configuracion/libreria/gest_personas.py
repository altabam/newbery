from datetime import datetime

from  configuracion.models import Personas
from django.http import  HttpResponse,HttpResponseBadRequest
from django.core import serializers

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def cargarPersona(row):
    model = Personas()
    print("nombre:"+ row[2])
    print("fecha_nac:"+ row[3])
    id =Personas.objects.order_by('id').last().id+1
    if id:
        model.id = id
    else:
        model.id = 1
    model.dni=row[0]
    model.apellido=row[1]
    model.nombre =row[2]
    if row[3] != "":
        model.fecha_nacimiento=datetime.strptime(row[3], '%d/%m/%Y').date()
    model.telefono=row[4]
    model.direccion=row[5]
    model.save(force_insert=True)

def buscarPersona(request):
    if not (is_ajax(request=request) or request.method != "GET"):
        print("entra aqui")
        print (is_ajax(request=request))
       # print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    print("valor de q:", valor)           #  otra forma de buscar seria cambiar "istartswith" por "icontains"
    personas = Personas.objects.filter(apellido__istartswith= valor)
    data = serializers.serialize('json', personas,use_natural_foreign_keys=True)
    return HttpResponse(data, content_type="application/json") 
