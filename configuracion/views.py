from django.shortcuts import render
from datetime import datetime
import csv
from django.db.models import Count
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

    cargarCategorias()

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
        cargarPersona(row)

    return render (request, "cargaInicial.html")

def cargarPersona(row):
    model = Personas()
    j = len(Personas.objects.all())
    print("nombre:"+ row[2])
    print("fecha_nac:"+ row[3])
    model.dni=row[0]
    model.apellido=row[1]
    model.nombre =row[2]
    if row[3] != "":
        model.fecha_nacimiento=datetime.strptime(row[3], '%d/%m/%Y').date()
    model.telefono=row[4]
    model.direccion=row[5]
    model.save(force_insert=True)
    
def cargarSocio(reader):
    persona = Personas.objects.get(dni=reader)
    socio = Socios()
    socio.numero =len(Socios.objects.all())
    socio.persona = persona
    socio.responsable = 'S'
    socio.save(force_insert=True)


def cargaMasivaSocios(request):
    template_name = "configuracion/migrations/socios.csv"
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

    return render (request, "cargaMasiva.html")

def cargaMasiva(request):
    return render (request, "cargaMasiva.html")


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
        j = len(Personas.objects.all())
        print(j)
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
           j= j+1
    
    listadoCategorias = Categorias.objects.all();

    contexto ={ "listadoCategorias": listadoCategorias, "mensaje":mensaje } 
    return render (request, "gestionarJugadoresCategoria.html",contexto)

def cargarJugador(persona,categoria):
    model = Jugadores()
    print(categoria)
    j = len(Jugadores.objects.all())
    model.id=j
    model.persona=persona
    model.categoria=categoria
    model.save(force_insert=True)
    
def cargarCategoriasArchivo():
    template_name = "configuracion/migrations/categorias.csv"
    model = Categorias()
    Categorias.objects.all().delete()
    with open (template_name) as f:
        j = 1
        reader = csv.reader(f )
        for row in reader:
            if not Categorias.objects.filter(nombre = row[0]).exists():
              model.id= j
              model.nombre =row[0]
              model.disciplina=Disciplinas.objects.get(id=row[1])
              model.save(force_insert=True)
              j= j+1
            else:
                print("categoria: "+ row+ " existe")


def cargarCategorias(request):
    cargarCategoriasArchivo()
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje } 
    return render (request, "cargaMasiva.html",contexto)