import csv
from django.shortcuts import render,redirect

from configuracion.models import Socios, Personas
from  .gest_personas import cargarPersona

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
    
    contexto =  { "datos": "preuba", }
    return render(request, "agruparSocios.html", contexto ) 