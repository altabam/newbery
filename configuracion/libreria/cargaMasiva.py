from django.shortcuts import render, redirect
import csv
from configuracion.models import IntegrantesClub, Personas, BecasJugador, Jugadores, CalidadIntegrante, BecasMotivos, Becas

from .gest_socios import cargarSociosCsv

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
            calidadIntegrante = CalidadIntegrante.objects.get(id=row[1])
            if persona:
                if  not IntegrantesClub.objects.filter(persona = persona).exists():
                    if IntegrantesClub.objects.last():
                        model.id = IntegrantesClub.objects.last().id+1
                    else:
                        model.id = 1

                    model.persona = persona
                    model.calidad = calidadIntegrante
                    model.save(force_insert=True)
                else:
                        print(row)
            else:
                print("Persona:", row[0], "no existe" )
                
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)


def cargaBecasJugadores(request):
    template_name = "configuracion/migrations/becasJugador.csv"
    model = BecasJugador()
    mensaje ="carga con exito"
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            persona = Personas.objects.get(dni = row[0])
            jugador = Jugadores.objects.get(persona = persona)
            solicita = Personas.objects.get(dni = row[5])
            if jugador:
                if  not BecasJugador.objects.filter(jugador = jugador).exists():
                    if BecasJugador.objects.last():
                        model.id = BecasJugador.objects.last().id+1
                    else:
                        model.id = 1

                    model.jugador = jugador
                    model.beca = Becas.objects.get(id=row[1])
                    model.anio = row[2]
                    model.mesDesde = row[3]
                    model.mesHasta = row[4]
                    model.solicita = IntegrantesClub.objects.get(persona = solicita)
                    model.motivoSolicitud = BecasMotivos.objects.get(id=row[6])
                    model.save(force_insert=True)
                else:
                        print("Beca de: ", row ," existe")
            else:
                print("Jugador:", row[0], "no existe" )
                mensaje ="Jugador:"+ row[0]+ " no existe" 
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)


