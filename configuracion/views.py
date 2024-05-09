from django.shortcuts import render
from datetime import datetime
import csv

from configuracion.models import Personas, Disciplinas, Categorias, Jugadores, Becas, Socios

# Create your views here.
def listadoPersonas(request):
    
    listadoPersona = Personas.objects.all()
    print(listadoPersona)
    contexto = { "listadoPersonas": listadoPersona }
    return render(request, "personas.html",  contexto)

def listadoDisciplinas(request):
    listadoDisciplina = Disciplinas.objects.all()
    print(listadoDisciplina)
    contexto =  { "listadoDisciplinas": listadoDisciplina, }
    
    return render(request, "disciplinas.html",  contexto)

def listadoCategorias(request):
    listadoCategoria = Categorias.objects.all()
    print(listadoCategoria)
    contexto =   { "listadoCategorias": listadoCategoria }
    
    return render(request, "categorias.html",  contexto)

def listadoJugadores(request):
    listadoJugador = Jugadores.objects.all()
    print("paso")
    print(listadoJugador)
    contexto ={ "listadoJugadores": listadoJugador }
    return render(request, "jugadores.html",  contexto)

def listadoBecas(request):
    listadoBeca = Becas.objects.all()
    print(listadoBeca)
    contexto ={ "listadoBecas": listadoBeca, }
    
    return render(request, "becas.html",  contexto)

def listadoSocios(request):
    listadoSocio = Socios.objects.all()
    print(listadoSocio)
    contexto ={ "listadoSocios": listadoSocio, }
    
    return render(request, "socios.html",  contexto)


def cargaInicial (request):
    template_name = "configuracion/migrations/disciplinas.csv"
    model = Disciplinas()
    Disciplinas.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            model.nombre =row[0]
            model.save(force_insert=True)
            j= j+1

    template_name = "configuracion/migrations/categorias.csv"
    model = Categorias()
    Categorias.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            model.nombre =row[0]
            model.disciplina=Disciplinas.objects.get(id=row[1])
            model.save(force_insert=True)
            j= j+1
    template_name = "configuracion/migrations/becas.csv"
    model = Becas()
    Becas.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            model.nombre =row[0]
            model.porcentaje=id=row[1]
            model.save(force_insert=True)
            j= j+1
    template_name = "configuracion/migrations/personas.csv"
    model = Personas()
    Personas.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            print("fecha_nac:"+str(row[0]))
            model.dni=row[0]
            model.apellido=row[1]
            model.nombre =row[2]
            print("fecha_nac:"+str(len(row[3])))
            if row[3] != "":
              model.fecha_nacimiento=datetime.strptime(row[3], '%d/%m/%Y').date()
            model.telefono=row[4]
            model.direccion=row[5]
            model.save(force_insert=True)
            j= j+1

    template_name = "configuracion/migrations/jugadores.csv"
    model = Jugadores()
    Jugadores.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            print(row[1], Categorias.objects.get(id=row[1]))
            model.persona=Personas.objects.get(id=row[0])
            model.categoria=Categorias.objects.get(id=row[1])
            model.save(force_insert=True)
            j= j+1
    
    template_name = "configuracion/migrations/socios.csv"
    model = Socios()
    Socios.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            model.id= j
            model.numero=row[0]
            model.personas=Personas.objects.get(id=row[1])
            model.save(force_insert=True)
            j= j+1

    return render (request, "cargaInicial.html")

def cargaMasivaSocios(request):
    template_name = "configuracion/migrations/socios.csv"
    model = Socios()
    with open (template_name) as f:
        j = len(Socios.objects.all())
        print(j)
        reader = csv.reader(f )
        for row in reader:
           # model.nombre =row[0]
           # model.save(force_insert=True)
            j= j+1

    return render (request, "cargaMasiva.html")

def cargaMasiva(request):
    return render (request, "cargaMasiva.html")
