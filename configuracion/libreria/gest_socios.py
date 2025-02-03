import csv
from django.utils import timezone
from django.shortcuts import render, redirect
from django.http import  HttpResponse,HttpResponseBadRequest
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta

from home.views import ObtenerMenu



from configuracion.models import Socios, Personas
from .gest_personas import cargarPersona

    
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
           print(row)
           try:
              persona = Personas.objects.get(dni=row[0])
              if  Socios.objects.filter(persona = persona).exists():
                 print("socio existe")
              else: 
                 print("socio no existe")
                 cargarSocio(row[0])
           except Personas.DoesNotExist:
              cargarPersona(row)
              cargarSocio(row[0])
              pass

           # model.save(force_insert=True)
           j= j+1


def cargarSocio(reader):
    persona = Personas.objects.get(dni=reader)
    socio = Socios()
    socio.numero =len(Socios.objects.all())
    socio.persona = persona
    socio.responsable = 'S'
    user = User.objects.create_user(persona.dni, persona.email, persona.dni)
    user.first_name = persona.nombre
    user.last_name = persona.apellido
    user.save()
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
    contexto =  { "datos": "Buscar Socios responsables",                   "menu": ObtenerMenu(request.user), 
    }
    return render(request, "agruparSocios.html", contexto ) 


def buscarSocioResponsable(request):
    if not (is_ajax(request=request) or request.method != "POST"):
        print (is_ajax(request=request))
        print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    #print("valor de q:", valor)                  otra forma de buscar seria cambiar "istartswith" por "icontains"
    socios = Socios.objects.filter(persona__apellido__istartswith= valor, responsable='S')
    print(socios)
    data = serializers.serialize('json', socios,use_natural_foreign_keys=True)
    print(data)
    return HttpResponse(data, content_type="application/json") 

def buscarSocio(request):
    if not (is_ajax(request=request) or request.method != "POST"):
        print (is_ajax(request=request))
        print (request.method != "POST")
        return HttpResponseBadRequest()
    valor = request.GET['q']
    #print("valor de q", valor)
    socios = Socios.objects.filter(persona__apellido__startswith= valor)
    data = serializers.serialize('json', socios,use_natural_foreign_keys=True)
    print(data)
    return HttpResponse(data, content_type="application/json")  

def listarIntegrantesSocios(request, id):
    socio = Socios.objects.get(pk =id)
    print(socio)
    listadoIntegrantes = Socios.objects.filter(numero = socio.numero, responsable="N") 
    contexto =  { "responsable": socio,
                 "listadoIntegrantes":listadoIntegrantes,
                 "menu": ObtenerMenu(request.user), 

    }
    return render(request, "integrantesSocios.html", contexto ) 


""" Funcion para agregar integrante a grupo social """
def agregarIntegranteSocio(request,id,idpk):
    responsable = Socios.objects.get(id=idpk)
    
    model = Socios()
    model.id = Socios.objects.last().id + 1
    model.numero = responsable.numero
    model.persona = Personas.objects.get(id=id)
    model.responsable ="N"
    model.fecha_alta = timezone.now()
    model.save(force_insert=True)

    socios = Socios.objects.all()
    personas = Personas.objects.exclude(id__in=([p.persona.id for p in socios]))
    contexto =  { "responsable": responsable,
                 "listadoPersonas":personas,
                 "titulo":'Agregar Integrante a cargo de:',
                 "menu": ObtenerMenu(request.user), 

    }
    return render(request, "personasNoSocias.html", contexto) 
  
def quitarIntegranteSocio(request,id,idpk):
    socio = Socios.objects.get(pk =idpk)
    Socios.objects.get(pk=id).delete()
    print(socio)
    listadoIntegrantes = Socios.objects.filter(numero = socio.numero, responsable="N") 
    contexto =  { "responsable": socio,
                 "listadoIntegrantes":listadoIntegrantes,
                 "menu": ObtenerMenu(request.user), 
    }
    return render(request, "integrantesSocios.html", contexto ) 

def listarIntegrantesSinSocio(request,id):
    responsable = Socios.objects.get(id=id)
    integrantes = Socios.objects.filter(numero = responsable.numero, responsable="N")
    socios = Socios.objects.all()
    persona_buscar=request.GET.get('apellido', '')
    personas = Personas.objects.exclude(id__in=([p.persona.id for p in socios]))

    if persona_buscar:
        personas=personas.filter(apellido__icontains=persona_buscar)
    contexto =  { "responsable": responsable,
                 "listadoSocios":personas,
                 "integrantes": integrantes,
                 'persona_buscar':persona_buscar,
                  "menu": ObtenerMenu(request.user), 
    }
    return render(request, "personasNoSocias.html", contexto ) 

def listarPersonasNoSocios(request):
    socios=Socios.objects.all()
    persona_buscar=request.GET.get('apellido', '')
    # Calcular la fecha límite para ser mayor de 18 años
    fecha_limite = datetime.now().date() - timedelta(days=18*365)
    personas = Personas.objects.exclude(
        id__in=([p.persona.id for p in socios])
    ).filter(
        fecha_nacimiento__lte=fecha_limite
    ).exclude(    # Excluir personas que ya son socios, que son menores de 18 años o que no tienen fecha de nacimiento.
        fecha_nacimiento__isnull=True
    ).order_by('apellido')
    if persona_buscar:
        personas=personas.filter(apellido__icontains=persona_buscar)
    contexto =  { 
                 "listadoPersonas":personas,
                 'titulo': 'Agregar Nuevo Socio',
                 "url_dinamica": '',
                 'persona_buscar':persona_buscar,
                  "menu": ObtenerMenu(request.user), 
    }
    return render(request, "personasNoSocias.html", contexto ) 

def agregarNuevoSocio(request, id):
    persona = Personas.objects.get(id=id)

    #le damos un numero de socio, que será el que le sigue del ultimo existente en la lista de socios.
    ultimoSocio = Socios.objects.order_by('-numero').first()
    nuevoNumero = (ultimoSocio.numero +1) if ultimoSocio else 1

    #crear nuevo socio
    nuevoSocio= Socios(
        numero=nuevoNumero,
        persona= persona,
        responsable= "S",
        fecha_alta = timezone.now()
    )
    nuevoSocio.save()
    return redirect('/configuracion/listadoSocios')

def eliminarSocioResponsable(request, id): #Eliminar socios de forma DEFINITIVA base de datos.
    socio= Socios.objects.filter(id=id).delete()
    listadoSocios = Socios.objects.all()

    contexto = {'listadoSocios':listadoSocios,                  "menu": ObtenerMenu(request.user), 
    }
    return render(request, 'socios.html', contexto)
