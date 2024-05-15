from django.shortcuts import render, redirect
from django.http import  HttpResponse, JsonResponse,HttpResponseBadRequest
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from  configuracion.models import Socios
import json

# Create your views here.

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)
    

def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def render_cobros(request):
    
    return render(request, "cobros.html", )
    
def busqueda_socio(request):

    if not (is_ajax(request=request) or request.method != "POST"):
        print (is_ajax(request=request))
        print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    print("valor de q", valor)
    socios = Socios.objects.filter(persona__apellido__startswith= valor)
    
    user_fields = (
        'numero',
        'personas',
        'nombre',
    )

    data = serializers.serialize('json', socios,use_natural_foreign_keys=True,cls=LazyEncoder)
    print(data)
    return HttpResponse(data, content_type="application/json") 
