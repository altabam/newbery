from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static
import csv
from django.http import JsonResponse
from django.db.models import Count, Subquery
from django.core.exceptions import ObjectDoesNotExist   
from .models import Personas, Disciplinas, Categorias, Jugadores, Becas, Socios, Cuotas, BecasJugador, BecasMotivos, CalidadIntegrante, IntegrantesClub
from .forms import PersonaForm, DisciplinasForm, CategoriasForm, JugadoresCategoriasForm,borrarJugadorForm
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
    contexto =  { "listadoDisciplinas": listadoDisciplina }
    return render(request, "disciplinas.html",  contexto)

def listadoCategorias(request):
    listadoCategoria = Categorias.objects.all()#filter(activo=True)
    contexto =   { "listadoCategorias": listadoCategoria }
    return render(request, "categorias.html",  contexto)

def listarJugadoresNoSocios(request):
    socios= Socios.objects.filter(fecha_baja = None).values()
    id=[]
    for socio in socios:
        print (socio.get('persona_id'))
        id.append(socio.get('persona_id'))
    print(id)
    listarJugadoresNoSocios =Jugadores.objects.exclude(persona_id__in = id)
    contexto =   { "listarJugadoresNoSocios": listarJugadoresNoSocios }
    return render(request, "listarJugadoresNoSocios.html",  contexto)

def listadoJugadores(request):

    # Obtener todas las disciplinas y categorias disponibles
    disciplinas = Disciplinas.objects.all()
    categorias = Categorias.objects.filter(activo= True)

    disciplinaId = request.GET.get('disciplina') #obtenemos el valor del select
    categoriaId = request.GET.get('categoria')
    listadoJugador = Jugadores.objects.filter(activo=True).order_by('categoria__disciplina','categoria')

    # Si se proporciona un ID de disciplina, filtrar
    if disciplinaId:
        listadoJugador = listadoJugador.filter(categoria__disciplina_id=disciplinaId)
        categorias = categorias.filter(disciplina_id= disciplinaId) #en base a la disciplina seleccionada filtra la categoria.

    if categoriaId:
        listadoJugador = listadoJugador.filter(categoria_id=categoriaId)
    contexto ={ 
        "listadoJugadores": listadoJugador,
        'disciplinas': disciplinas,
        'categorias':categorias }
    result = (Jugadores.objects
        .values('categoria')
        .annotate(dcount=Count('categoria'))
        .order_by()
    )
    print (result)

    return render(request, "jugadores.html",  contexto)

def listadoBecas(request):
    listadoBeca = Becas.objects.all()
    contexto ={ "listadoBecas": listadoBeca, }
    
    return render(request, "becas.html",  contexto)

def listadoSocios(request):
    listadoSocio = obtenerSocios().filter(responsable= "S")
    contexto ={ "listadoSocios": listadoSocio, }
    
    return render(request, "socios.html",  contexto)


def listarCuotas(request):
    listadoCuotas = Cuotas.objects.all().order_by("fecha_hasta","cant_int")
    contexto ={ "listadoCuotas": listadoCuotas, }
    return render(request, "cuotas.html",  contexto)

def listarMotivoBecas(request):
    listadoMotivosBecas = BecasMotivos.objects.all()
    contexto ={ "listadoMotivosBecas": listadoMotivosBecas, }
    return render(request, "motivosBecas.html",  contexto)

def listarMotivoCalicadIntegrantes(request):
    listadoCalidadIntegrantes = CalidadIntegrante.objects.all()
    contexto ={ "listadoCalidadIntegrantes": listadoCalidadIntegrantes, }
    return render(request, "calidadIntegrantes.html",  contexto)

def listarIntegrantesClub(request):
    listadoIntegranteClub = IntegrantesClub.objects.all()
    print(listadoIntegranteClub)
    contexto ={ "listadoIntegranteClub": listadoIntegranteClub, }
    return render(request, "integrantesClub.html",  contexto)


def cargaInicial (request):
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
             if  Jugadores.objects.filter(persona = persona, categoria=categoria).exists():
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
            #aqui inicia codigo de prueba
            nombre_categoria = row[0]
            id_disciplina = row[1]
            
            if not Categorias.objects.filter(nombre=nombre_categoria).exists():
                try:
                    disciplina = Disciplinas.objects.get(id=id_disciplina)
                    nueva_categoria = Categorias(
                        nombre=nombre_categoria,
                        disciplina=disciplina
                    )
                    nueva_categoria.save()
                    print(f"Categoría {nombre_categoria} agregada con éxito.")
                except ObjectDoesNotExist:
                    print(f"Disciplina con id {id_disciplina} no existe. No se pudo agregar la categoría {nombre_categoria}.")
            else:
                print(f"Categoría {nombre_categoria} ya existe.")
            #if not Categorias.objects.filter(nombre = row[0]).exists():
            #  model.id = Categorias.objects.last().id+1
             # model.nombre =row[0]
             # model.disciplina=Disciplinas.objects.get(id=row[1])
             # model.save(force_insert=True)
           # else:
            #    print("categoria: "+ row[0]+ " existe")


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
           form.id = id =Personas.objects.order_by('id').last().id+1
           form.save()
           return redirect('/configuracion/listadoPersonas')
    else:
        form =PersonaForm()

    contexto ={ 
            "accion":"Agregar", 
            "form": form,
         } 
    return render(request, "editarPersona.html", contexto )    

#Vistas de acciones sobre Disciplinas
def agregarDisciplinas(request):
    if request.method == 'POST':
        form= DisciplinasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoDisciplinas')
    else:
        form =DisciplinasForm()
    
    return render(request, 'agregarDisciplinas.html', {'form': form})

def editarDisciplinas(request,id):
    disciplina = Disciplinas.objects.get(id = id)
    categorias_activas= Categorias.objects.filter(disciplina=disciplina, activo=True).exists()
    jugadores_activos= Jugadores.objects.filter(categoria__disciplina=disciplina, activo=True).exists()
    if categorias_activas or jugadores_activos:
        return render(request, 'mensaje.html', {
            'mensaje': 'No se puede editar esta disciplina porque tiene jugadores y/ o categorias activos.',
            'url_redireccion': '/configuracion/listadoDisciplinas',
        })
    if request.method == 'POST':
        form= DisciplinasForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoDisciplinas')
    else:
            form = DisciplinasForm( instance=disciplina)

    contexto ={ 
            "accion":"Modificar", 
            "form": form,
            "datos": disciplina,
         } 
    return render(request, "editarDisciplina.html",contexto)

def borrarLogDisciplinas(request,id):
    disciplina = get_object_or_404(Disciplinas, id=id)
    categorias_activas= Categorias.objects.filter(disciplina=disciplina, activo=True).exists()
    jugadores_activos= Jugadores.objects.filter(categoria__disciplina=disciplina, activo=True).exists()
    if categorias_activas or jugadores_activos:
        return render(request, 'mensaje.html', {
            'mensaje': 'No se puede borrar esta disciplina porque tiene jugadores y/ o categorias activos.',
            'url_redireccion': '/configuracion/listadoDisciplinas',
        })
    if request.method == 'POST':
        disciplina.activo= False
        disciplina.save()
        return redirect('/configuracion/listadoDisciplinas')
    cancel_url =  '/configuracion/listadoDisciplinas'
    return render(request, 'alert.html', {'cancel_url': cancel_url})

def borrarDisciplinas(request, id):  # Permite borrar Disciplinas DEFINITIVAMENTE de base de datos, NO SE USA
    Disciplinas.objects.filter(id=id).delete()
    listadoDisciplinas = Disciplinas.objects.all()
    contexto = { "listadoDisciplinas": listadoDisciplinas }
    return render(request, "disciplinas.html",  contexto)

#Vistas de acciones sobre Categorias
def agregarCategorias(request):
    if request.method == 'POST':
        form= CategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoCategorias')
    else:
        form =CategoriasForm()
    contexto = {
        'form': form,
        'titulo': 'Agregar Categoría',
        'boton_texto': 'Agregar Categoría',
    }
    return render(request, 'agregarCategorias.html', contexto)

def editarCategorias(request,id):
    categoria = Categorias.objects.get(id=id)
    jugadores_activos = Jugadores.objects.filter(categoria=categoria, activo=True).exists()

    if request.method == 'POST':
        form = CategoriasForm(request.POST, instance=categoria)
        if form.is_valid():
            print ("hola1 ")
            if not jugadores_activos:  # Solo guardamos si no hay jugadores activos
                form.save()
            return redirect('/configuracion/listadoCategorias')
    else:
        form = CategoriasForm(instance=categoria)
        if jugadores_activos:  # Removemos el campo si hay jugadores activos
            form.fields.pop('activo')
    contexto = {
        "accion": "Modificar",
        "form": form,
        "datos": categoria,
    }
    return render(request, "editarCategoria.html", contexto)

def borrarLogCategorias(request,id):
    categoria = get_object_or_404(Categorias, id=id)
    jugadores_activos= Jugadores.objects.filter(categoria=categoria, activo=True).exists()
    if jugadores_activos:
        return render(request, 'mensaje.html', {
            'mensaje': 'No se puede borrar esta categoria porque tiene jugadores activos.',
            'url_redireccion': '/configuracion/listadoCategorias',
        })
    if request.method == 'POST':
        categoria.activo= False
        categoria.save()
        return redirect('/configuracion/listadoCategorias')  
    cancel_url =  '/configuracion/listadoCategorias'
    return render(request, 'alert.html', {'cancel_url': cancel_url})
    

def borrarCategorias(request,id):   # Permite borrar categorias DEFINITIVAMENTE de base de datos, NO SE USA
    Categorias.objects.filter(id=id).delete()
    listadoCategorias = Categorias.objects.all()
    contexto = { "listadoCategorias": listadoCategorias }
    return render(request, "categorias.html",  contexto)

#vistas de acciones sobre jugadores de categorias
def agregarJugadorCategorias(request):
    categorias = Categorias.objects.filter(activo= True)

    if request.method == 'POST':
        form= JugadoresCategoriasForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoJugadores')
        else:
            #Recarga las categorias dinamicamente en caso de un error de formulario
            disciplina_id = request.POST.get('disciplina') #Por ejemplo, si el usuario cambia la disciplina
            if disciplina_id:      
                form.fields['categoria'].queryset = categorias.filter(disciplina_id=disciplina_id) 
    else:
        form =JugadoresCategoriasForm()
    contexto = {
        'form': form,
        'titulo': 'Agregar Jugador a Categoría',
        'boton_texto': 'Agregar Jugador',
    }
    return render(request, 'agregarJugadorCategorias.html', contexto) 
    
def obtenerCategorias(request):
    categorias = Categorias.objects.filter(activo= True)
    disciplina_id = request.GET.get('disciplina_id')
    categorias = categorias.filter(disciplina__id=disciplina_id)
    return JsonResponse(list(categorias.values()), safe=False)

def obtener_personas(request):
    term = request.GET.get('term', '')
    personas = Personas.objects.filter(dni__icontains=term)
    results = [{'id': persona.id, 'text': persona.dni} for persona in personas]
    return JsonResponse(results, safe=False)


def editarJugadorCategorias(request,id):
    jugador = get_object_or_404(Jugadores, id=id)
    if request.method == 'POST':
        form= JugadoresCategoriasForm(request.POST, instance=jugador)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listadoJugadores')
    else: 
        form = JugadoresCategoriasForm( instance=jugador)
    contexto={
        "accion":"Modificar", 
        "form": form,
        "datos": jugador,
        "titulo": 'Editar Jugador',
    }
    return render(request, "agregarJugadorCategorias.html",contexto)

def borrarJugadorLogCategorias(request, id):
    jugador = get_object_or_404(Jugadores, id=id)
 
    if request.method == 'POST':
        fecha_hasta = request.POST.get('fecha_hasta')
        if fecha_hasta:
            jugador.activo = False
            jugador.fecha_hasta = fecha_hasta
            jugador.save()
            return redirect('/configuracion/listadoJugadores')
    
    return render(request, 'borrarJugadorCategorias.html')
   


def borrarJugadorCategorias(request, id):   # Permite borrar Jugadores DEFINITIVAMENTE de base de datos, NO SE USA 
    Jugadores.objects.filter(id=id).delete()
    listadoJugadores = Jugadores.objects.all
    contexto ={'listadoJugadores': listadoJugadores}
    return render(request,'Jugadores.html', contexto)

