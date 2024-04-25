from django.shortcuts import render
from configuracion.models import Personas, Disciplinas, Categorias, JugadoresCategoria, Becas

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
    listadoCategoria = Categorias.objects.all()
    print(listadoCategoria)
    contexto =[
        { "listadoCategorias": listadoCategoria }
    ]
    return render(request, "categorias.html",  contexto)

def listadoBecas(request):
    listadoBeca = Becas.objects.all()
    print(listadoBeca)
    contexto ={ "listadoBecas": listadoBeca, }
    
    return render(request, "becas.html",  contexto)
