from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.db.models import Count, Subquery
from datetime import date
import calendar
from django.core.exceptions import ObjectDoesNotExist   
from .models import AsistenciaEventoDeportivo

from home.views import ObtenerMenu
from configuracion.models import IntegrantesClub,IntegrantesClubCategorias, Jugadores,EventoDeportivo

#from .forms import PersonaForm, DisciplinasForm, CategoriasForm, JugadoresCategoriasForm,borrarJugadorForm

# Create your views here.
def listarAsistencia(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    eventosDep = EventoDeportivo.objects.all()

    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Asistencia de Jugadores",
                 "anio": date.today().year,
                 "mes" : date.today().month,
                 "dia" : 0,
                 "eventosDeportivos": eventosDep,
                 "categoriaSele": 0,
                 "fechaEntrenamientoSele":"-",
                 "eventoDeportivoSele":0 ,
               }
    return render(request, "listarAsistencia.html",  contexto)


def filtrarAsistenciaJugadoresCategoria(request, anio, mes, accion, categoria, fechaEntrenamiento, evento  ):
    #accion 0-mantener mer  1-incrementar mes   2-decrementar mes
    #anio = date.today().year
    #mes = date.today().month
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
   # print(" Integrante Club:", intClubCat.all().get().categorias)
    print("HOLA")
    eventosDep = EventoDeportivo.objects.all()
    jugadores = Jugadores.objects.filter(categoria = intClubCat.all().get().categorias)
    matrizAsistencia= []
    matrizJugador= []
    if (accion==2):
       if (mes ==1):
          mes = 12
          anio -=1
       else:
          mes -=1
    elif(accion==1):
       if (mes ==12):
          mes = 1
          anio +=1
       else:
          mes +=1
       
    ultDiaMes = calendar.monthrange(anio, mes)[1] +1
    for dia in range(0, ultDiaMes):
      matrizJugador.append(dia)
    matrizAsistencia.append(matrizJugador)
    matrizJugador=[]
    for jug in jugadores:
      matrizJugador.append(jug.persona.apellido+" "+jug.persona.nombre)
      for dia in range(1, ultDiaMes):
          #print(dia)
          asistencia = AsistenciaEventoDeportivo.objects.filter(fecha=date(anio,mes, dia), jugador = jug)
          if asistencia.exists():
    #        print( jug, asistencia.get().asiste)
            matrizJugador.append(asistencia.get().asiste)
          else: 
            matrizJugador.append('')
      matrizAsistencia.append(matrizJugador)
      matrizJugador=[]
        
    cantElemFila= len(matrizAsistencia[0])
    #print (request.GET['fechaEntrenamiento'])
    if request.GET:
       if request.GET["categoria"]=="":
         categoriaSele =0
       else:      
         categoriaSele = request.GET["categoria"]
       if request.GET["fechaEntrenamiento"]=="":
         fechaEntrenamientoSele = "a"
       else:
          fechaEntrenamientoSele = request.GET["fechaEntrenamiento"]
       if request.GET["eventoDeportivo"]=="":
         eventoDeportivoSele = 0
       else:
         eventoDeportivoSele = request.GET["eventoDeportivo"]
       print("datos parametros:",categoriaSele, fechaEntrenamientoSele, eventoDeportivoSele)
    else:
       categoriaSele = categoria
       fechaEntrenamientoSele = fechaEntrenamiento
       eventoDeportivoSele = evento
       

    
       
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Asistencia de Jugadores",
                 "eventosDeportivos": eventosDep,
                 "anio": anio,
                 "mes" : mes,
                 "dia" : dia,
                 "cantElemFila":cantElemFila,
                 "matrizAsistencia" :matrizAsistencia,
                 "categoriaSele": categoriaSele,
                 "fechaEntrenamientoSele":fechaEntrenamientoSele,
                 "eventoDeportivoSele":eventoDeportivoSele 
               }
    return render(request, "listarAsistencia.html",  contexto)


def cargarAsistencia(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Cargar Asistencia de Jugadores",
                 "boton_texto": "Cargar Asistencia",
               }
    return render(request, "cargarAsistencia.html",  contexto)


def filtrarJugadoresCategoria(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    eventosDep = EventoDeportivo.objects.all()
    categoriaId = request.GET.get('categoria')
    if categoriaId:
        listadoJugadores = Jugadores.objects.filter(categoria_id=categoriaId)
    else:
        listadoJugadores ={}
    print(listadoJugadores)
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Cargar Asistencia de Jugadores",
                 "boton_texto": "Cargar Asistencia",
                 "listadoJugadores" : listadoJugadores,
                 "eventosDeportivos" : eventosDep,
               }
    return render(request, "cargarAsistencia.html",  contexto)

def cargarAsistenciaJugadoresCategoria(request):
  print(request.POST)
  print("paso por cargarAsistencia")

  if not AsistenciaEventoDeportivo.objects.filter(fecha= request.POST['fechaEntrenamiento']).exists():
    for  jugador in request.POST.getlist('jugadores'):
      jug = Jugadores.objects.get(id = jugador)
      eve = EventoDeportivo.objects.get(id = request.POST['eventoDeportivo'])
      AsistenciaEventoDeportivo.objects.create(fecha= request.POST['fechaEntrenamiento'], jugador= jug, evento=eve)
      print (jug)
      
  print("para revisar")
  return filtrarJugadoresCategoria(request)
