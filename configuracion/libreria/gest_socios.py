import csv
from django.utils import timezone
from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseBadRequest
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder



from configuracion.models import Socios, Personas
from  .gest_personas import cargarPersona

class LazyEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, YourCustomType):
            return str(obj)
        return super().default(obj)
    
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def obtenerSocios():
    return Socios.objects.all().order_by("numero")


def cargarSociosCsv(url):
    template_name = url
    with open (template_name) as f:
        j = len(Socios.objects.all())
        print(j)
        reader = csv.reader(f )
        for row in reader:
           persona = Personas.objects.get(dni=row[0])
           print(row)
           if persona :
              
             if  Socios.objects.filter(persona = persona).exists():
                 print("socio existe")
             else: 
                 print("socio no existe")
                 cargarSocio(row[0])
           else:
              cargarPersona(row)
              cargarSocio(row[0])

           # model.save(force_insert=True)
           j= j+1


def cargarSocio(reader):
    persona = Personas.objects.get(dni=reader)
    socio = Socios()
    socio.numero =len(Socios.objects.all())
    socio.persona = persona
    socio.responsable = 'S'
    socio.save(force_insert=True)

def cargarAgrupacionFamiliarSociosCsv(url):
    template_name = url
    model = Socios()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            personaResponsable = Personas.objects.get(dni= row[0])
            socio = Socios.objects.get(persona=personaResponsable, responsable='S') 
            personaFamiliar = Personas.objects.get(dni= row[1])
            if  not Socios.objects.filter(persona = personaFamiliar).exists():
              model.id = Socios.objects.last().id+1
              model.numero =socio.numero
              model.persona=personaFamiliar
              model.responsable= 'N'
              model.save(force_insert=True)
              
            else:
                print("Agrupacion Familiar, persona existe")
                print(row)

def agruparSocios(request):
    
    contexto =  { "datos": "Buscar Socios responsables", }
    return render(request, "agruparSocios.html", contexto ) 

def buscarSocioResponsable(request):
    if not (is_ajax(request=request) or request.method != "POST"):
        print (is_ajax(request=request))
        print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    print("valor de q", valor)
    socios = Socios.objects.filter(persona__apellido__startswith= valor, responsable='S')
    data = serializers.serialize('json', socios,use_natural_foreign_keys=True,cls=LazyEncoder)
    #print(data)
    return HttpResponse(data, content_type="application/json") 



def buscarSocio(request):
    if not (is_ajax(request=request) or request.method != "POST"):
        print (is_ajax(request=request))
        print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    print("valor de q", valor)
    socios = Socios.objects.filter(persona__apellido__startswith= valor)
    data = serializers.serialize('json', socios,use_natural_foreign_keys=True,cls=LazyEncoder)
    print(data)
    return HttpResponse(data, content_type="application/json") 

def listarIntegrantesSocios(request, id):
    socio = Socios.objects.get(pk =id)
    print(socio)
    listadoIntegrantes = Socios.objects.filter(numero = socio.numero, responsable="N") 
    contexto =  { "responsable": socio,
                 "listadoIntegrantes":listadoIntegrantes,
    }
    return render(request, "integrantesSocios.html", contexto ) 

def listarIntegrantesSinSocio(request,id):
    responsable = Socios.objects.get(id=id)
    integrantes = Socios.objects.filter(numero = responsable.numero, responsable="N")
    socios = Socios.objects.all()
    print([p.persona.id for p in socios])
    personas = Personas.objects.exclude(id__in=([p.persona.id for p in socios]))
    print(personas)
    contexto =  { "responsable": responsable,
                 "listadoPersonas":personas,
                 "integrantes": integrantes,
    }
    return render(request, "personasNoSocias.html", contexto ) 


def agregarIntegranteSocio(request,id,idpk):
    responsable = Socios.objects.get(id=idpk)
    socios = Socios.objects.all()
    personas = Personas.objects.exclude(id__in=([p.persona.id for p in socios]))
    
    model = Socios()
    model.id = Socios.objects.last().id + 1
    model.numero = responsable.numero
    model.persona = Personas.objects.get(id=id)
    model.responsable ="N"
    model.fecha_alta = timezone.now()
    model.save(force_insert=True)
    
    contexto =  { "responsable": responsable,
                 "listadoPersonas":personas,
    }
    return render(request, "personasNoSocias.html", contexto) 
  

def quitarIntegranteSocio(request,id,idpk):
    socio = Socios.objects.get(pk =idpk)
    Socios.objects.get(pk=id).delete()
    print(socio)
    listadoIntegrantes = Socios.objects.filter(numero = socio.numero, responsable="N") 
    contexto =  { "responsable": socio,
                 "listadoIntegrantes":listadoIntegrantes,
    }
    return render(request, "integrantesSocios.html", contexto ) 
