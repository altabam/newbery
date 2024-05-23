from django.shortcuts import render,redirect
import csv
from django.db.models import Count
from .models import Personas, Disciplinas, Categorias, Jugadores, Becas, Socios, Cuotas, BecasJugador, BecasMotivos, CalidadIntegrante
from .forms import PersonaForm
from .libreria.cargaMasiva import * 
from .libreria.gest_socios import *
from .libreria.gest_personas import *
from .libreria.gest_carga_inicial import *
# Create your views here.
def listadoPersonas(request):
    
    listadoPersona = Personas.objects.all().order_by('apellido','nombre')
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
    print(listadoJugador)
    contexto ={ "listadoJugadores": listadoJugador }
    result = (Jugadores.objects
        .values('categoria')
        .annotate(dcount=Count('categoria'))
        .order_by()
    )
    print (result)

    return render(request, "jugadores.html",  contexto)

def listadoBecas(request):
    listadoBeca = Becas.objects.all()
    print(listadoBeca)
    contexto ={ "listadoBecas": listadoBeca, }
    
    return render(request, "becas.html",  contexto)

def listadoSocios(request):
    listadoSocio = obtenerSocios()
    print(listadoSocio)
    contexto ={ "listadoSocios": listadoSocio, }
    
    return render(request, "socios.html",  contexto)



def listarCuotas(request):
    listadoCuotas = Cuotas.objects.all().order_by("cant_int")
    print(listadoCuotas)
    contexto ={ "listadoCuotas": listadoCuotas, }
    return render(request, "cuotas.html",  contexto)

def listarMotivoBecas(request):
    listadoMotivosBecas = BecasMotivos.objects.all()
    print(listadoMotivosBecas)
    contexto ={ "listadoMotivosBecas": listadoMotivosBecas, }
    return render(request, "motivosBecas.html",  contexto)

def listarMotivoCalicadIntegrantes(request):
    listadoCalidadIntegrantes = CalidadIntegrante.objects.all()
    print(listadoCalidadIntegrantes)
    contexto ={ "listadoCalidadIntegrantes": listadoCalidadIntegrantes, }
    return render(request, "calidadIntegrantes.html",  contexto)



def cargaInicial (request):
    """
    
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
        cargarPersona(row)
"""
    return render (request, "cargaInicial.html")


    




def borrarTodosSocios(request):
    Socios.objects.all().delete()
    return render (request, "cargaMasiva.html")


def gestionarJugadoresCategoria(request):
    listadoCategorias = Categorias.objects.all();
    contexto ={ "listadoCategorias": listadoCategorias,  } 
    return render (request, "gestionarJugadoresCategoria.html",contexto)

    
def borrarJugadoresCategoria(request, id):
    listadoCategorias = Categorias.objects.all();
    jugadores = Jugadores.objects.filter(categoria = id)
    jugadores.delete()
    contexto ={ "listadoCategorias": listadoCategorias,  } 
    return render (request, "gestionarJugadoresCategoria.html",contexto)

def cargarJugadoresCategoria(request,id):
    mensaje="cargado con exito"
    categoria = Categorias.objects.get(id = id)
    template_name = "configuracion/migrations/categoria"+categoria.nombre+".csv"
    print(template_name)
    with open (template_name) as f:
              
        reader = csv.reader(f )
        for row in reader:
           print(row)
           if Personas.objects.filter(dni = row[0]).exists():
             persona = Personas.objects.get(dni=row[0])
             if  Jugadores.objects.filter(persona = persona).exists():
                 print("Jugador: "+row[0]+" existe")
             else: 
                 print("Jugador : "+row[0]+" no existe")
                 cargarJugador(persona,categoria)
           else:
              cargarPersona(row)
              persona = Personas.objects.get(dni=row[0])
              cargarJugador(persona,categoria)

           # model.save(force_insert=True)
    listadoCategorias = Categorias.objects.all();
    contexto ={ "listadoCategorias": listadoCategorias, "mensaje":mensaje } 
    return render (request, "gestionarJugadoresCategoria.html",contexto)

def cargarJugador(persona,categoria):
    model = Jugadores()
    print(categoria)
    model.id = Jugadores.objects.last().id+1
    model.persona=persona
    model.categoria=categoria
    model.save(force_insert=True)
    
def cargarCategoriasArchivo():
    template_name = "configuracion/migrations/categorias.csv"
    model = Categorias()
    #Categorias.objects.all().delete()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            if not Categorias.objects.filter(nombre = row[0]).exists():
              model.id = Categorias.objects.last().id+1
              model.nombre =row[0]
              model.disciplina=Disciplinas.objects.get(id=row[1])
              model.save(force_insert=True)
            else:
                print("categoria: "+ row[0]+ " existe")


def cargaBecasJugador(request):
    template_name = "configuracion/migrations/becasJugador.csv"
    model = BecasJugador()
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
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaMasiva.html",contexto)  



def cargarCategorias(request):
    cargarCategoriasArchivo()
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaMasiva.html",contexto)


def cargaInicialDisciplinas(request):
    template_name = "configuracion/migrations/disciplinas.csv"
    model = Disciplinas()
    #Disciplinas.objects.all().delete()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
           if  not Disciplinas.objects.filter(nombre = row[0]).exists():
                model.id = Disciplinas.objects.last().id+1
                model.nombre =row[0]
                model.save(force_insert=True)
           else:
                print(row)
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)

def cargaInicialBecas(request):
    template_name = "configuracion/migrations/becas.csv"
    model = Becas()
    #Becas.objects.all().delete()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            if  not Becas.objects.filter(nombre = row[0]).exists():
              model.id = Becas.objects.last().id+1
              model.nombre =row[0]
              model.porcentaje=id=row[1]
              model.save(force_insert=True)
            else:
                print(row)
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)


def cargaInicialCategorias(request):
    cargarCategoriasArchivo()
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaInicial.html",contexto)

def cargarAgrupacionFamiliarSocios(request):
    cargarAgrupacionFamiliarSociosCsv("configuracion/migrations/agrupFamiliarSocios.csv")
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaMasiva.html",contexto)

def borrarSocio(request,id):
    Socios.objects.filter(id=id).delete()

def borrarPersona(request, id):
    Personas.objects.filter(id=id).delete()
    listadoPersonas = Personas.objects.all().order_by('apellido','nombre')
    contexto = { "listadoPersonas": listadoPersonas }
    return render(request, "personas.html",  contexto)

def editarPersona(request,id):
    persona = Personas.objects.get(id = id)
    if request.method == 'POST':
        form= PersonaForm(request.POST, instance=persona)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoPersonas')
    else:
            form = PersonaForm( instance=persona)
    
    contexto ={ 
            "accion":"Modificar", 
            "form": form,
            "datos": persona,
         } 
    return render(request, "editarPersona.html",contexto)

def agregarPersona(request):
    if request.method == 'POST':
        form= PersonaForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('/configuracion/listadoPersonas')
    else:
        form =PersonaForm()

    contexto ={ 
            "accion":"Agregar", 
            "form": form,
         } 
    return render(request, "editarPersona.html", contexto )    

       