from django.shortcuts import render
from configuracion.models import Personas, Disciplinas, Categorias, JugadoresCategoria, Becas
import csv

# Create your views here.
def listadoPersonas(request):
    
    listadoPersona = Personas.objects.all()
    print(listadoPersona)
    contexto = { "listadoPersona": listadoPersona }
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

def listadoJugadoresCategoria(request):
    listadoJugadoresCategoria = JugadoresCategoria.objects.all()
    print(listadoJugadoresCategoria)
    contexto ={ "listadoJugadoresCategorias": listadoJugadoresCategoria }
    return render(request, "categoriaJugadores.html",  contexto)

def listadoBecas(request):
    listadoBeca = Becas.objects.all()
    print(listadoBeca)
    contexto ={ "listadoBecas": listadoBeca, }
    
    return render(request, "becas.html",  contexto)

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


    return render (request, "cargaInicial.html")

