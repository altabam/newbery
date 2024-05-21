from django.shortcuts import render, redirect
import csv
from configuracion.models import IntegrantesClub, Personas

from .gest_socios import cargarSociosCsv

def prueba():
    persona = Personas.objects.get(id=1)
    print(persona.apellido)

def cargaMasivaSocios(request):
    cargarSociosCsv( "configuracion/migrations/socios.csv")
    return render (request, "cargaMasiva.html")

def cargaMasiva(request):
    return render (request, "cargaMasiva.html")



def cargaIntegrantesClub(request):
    template_name = "configuracion/migrations/integrantesClub.csv"
    model = IntegrantesClub()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            persona = Personas.objects.get(dni = row[0])
            if persona:
                if  not IntegrantesClub.objects.filter(concepto = row[0]).exists():
                    if IntegrantesClub.objects.last():
                        model.id = IntegrantesClub.objects.last().id+1
                    else:
                        model.id = 1

                    model.persona = persona
                    model.calidad = row[1]
                    model.save(force_insert=True)
                else:
                        print(row)
            else:
                print("Persona:", row[0], "no existe" )
                
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)


