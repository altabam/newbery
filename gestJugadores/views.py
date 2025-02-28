from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.db.models import Count, Subquery
from datetime import date
import calendar
from django.core.exceptions import ObjectDoesNotExist   
from .models import AsistenciaEventoDeportivo

from home.views import ObtenerMenu
from configuracion.models import IntegrantesClub,IntegrantesClubCategorias, Jugadores,EventoDeportivo,Categorias

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
    return filtrarAsistenciaJugadoresCategoria(request, date.today().year,date.today().month, 0, 0,"-", 0 )


def filtrarAsistenciaJugadoresCategoria(request, anio, mes, accion, categoria, fechaEntrenamiento, evento  ):
    #accion 0-mantener mer  1-incrementar mes   2-decrementar mes
    #anio = date.today().year
    #mes = date.today().month
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
    else:
       categoriaSele = int(categoria)
       print("categoria:",categoriaSele)
       fechaEntrenamientoSele = fechaEntrenamiento
       eventoDeportivoSele = evento

    print("categoria:",categoriaSele)
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
   # print(" Integrante Club:", intClubCat.all().get().categorias)
   # print("HOLA", categoria, fechaEntrenamiento, evento)
    eventosDep = EventoDeportivo.objects.all()
    if (categoriaSele == 0):
      cat = []
      for icc in intClubCat:
        cat.append(  icc.categorias)
      jugadores = Jugadores.objects.filter(categoria__in = cat)
      print (jugadores.last().categoria.id)
    else:
      jugadores = Jugadores.objects.filter(categoria = categoriaSele)

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
    print("datos parametros:",categoriaSele, fechaEntrenamientoSele, eventoDeportivoSele)
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
                 "eventoDeportivoSele":eventoDeportivoSele,
                 "mesHoy": date.today().month,
                 "diaHoy": date.today().day,
                 "anioHoy": date.today().year,
               }
    return render(request, "listarAsistencia.html",  contexto)


def cargarAsistencia(request,anio, mes, dia, categoria, fechaEntrenamiento, evento ):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    fechaCargar = str(anio)+"-"+str(mes)+"-"+str(dia)
    cat = Categorias.objects.get(id = categoria)
    eventosDep = EventoDeportivo.objects.all()
    matrizAsistencia= []
    matrizJugador= []

    if AsistenciaEventoDeportivo.objects.filter(fecha= fechaCargar).exists():
      jugadores = Jugadores.objects.filter(categoria = categoria)
      for jug in jugadores:
        asiste = AsistenciaEventoDeportivo.objects.filter(fecha= fechaCargar, jugador =jug)
        if asiste.exists():
            matrizJugador.append(asiste.get().asiste)
            matrizJugador.append(asiste.get().justifica)
            matrizJugador.append(asiste.get().jugador)
        else: 
            matrizJugador.append('No')
            matrizJugador.append('No')
            matrizJugador.append(jug)
        matrizAsistencia.append(matrizJugador)
        matrizJugador=[]

      #listadoJugadores = Jugadores.objects.filter(id_in = jug)

    else:
      jugadores = Jugadores.objects.filter(categoria = categoria)
      for jug in jugadores:
        matrizJugador.append('Si')
        matrizJugador.append('No')
        matrizJugador.append(jug)
        matrizAsistencia.append(matrizJugador)
        matrizJugador=[]

   # print(matrizAsistencia)
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Cargar Asistencia de Jugadores",
                 "boton_texto": "Cargar Asistencia",
                 "categoria": cat,
                 "fechaCargar": fechaCargar,
                 "eventosDeportivos" : eventosDep,
                 "matrizAsistencia" : matrizAsistencia,
                 "anio": anio,
                 "mes" : mes,
                 "dia" : dia,
                 "categoriaSele": categoria,
                 "fechaEntrenamientoSele":fechaEntrenamiento,
                 "eventoDeportivoSele":evento, 

               }
    return render(request, "cargarAsistencia.html",  contexto)


def filtrarJugadoresCategoria(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Cargar Asistencia de Jugadores",
                 "boton_texto": "Cargar Asistencia",
               }
    return render(request, "cargarAsistencia.html",  contexto)

def cargarAsistenciaJugadoresCategoria(request,categoria, fechaEntrenamiento):
  print(request.POST)

  if not AsistenciaEventoDeportivo.objects.filter(fecha= fechaEntrenamiento).exists():
    for  jugador in request.POST.getlist('asiste'):
      jug = Jugadores.objects.get(id = jugador)
      eve = EventoDeportivo.objects.get(id = request.POST['eventoDeportivo'])
      AsistenciaEventoDeportivo.objects.create(fecha= fechaEntrenamiento, jugador= jug, evento=eve, asiste='S')
      print (jug)
    for  jugador in request.POST.getlist('justifica'):
      jug = Jugadores.objects.get(id = jugador)
      eve = EventoDeportivo.objects.get(id = request.POST['eventoDeportivo'])
      AsistenciaEventoDeportivo.objects.create(fecha= fechaEntrenamiento, jugador= jug, evento=eve,justifica ='S')
      print (jug)
  else:
      eve = EventoDeportivo.objects.get(id = request.POST['eventoDeportivo'])
      for  jugador in request.POST.getlist('asiste'):
        jug = Jugadores.objects.get(id = jugador)
        if not AsistenciaEventoDeportivo.objects.filter(jugador = jug, fecha = fechaEntrenamiento).exists():
          AsistenciaEventoDeportivo.objects.create(fecha= fechaEntrenamiento, jugador= jug, evento=eve,asiste ='S')
        else:
          asist = AsistenciaEventoDeportivo.objects.get(jugador= jug, fecha = fechaEntrenamiento)
          asist.asiste ="S"
          asist.justifica="N"
          asist.evento = eve
          asist.save()

      for  jugador in request.POST.getlist('justifica'):
        jug = Jugadores.objects.get(id = jugador)
        if not AsistenciaEventoDeportivo.objects.filter(jugador = jug, fecha = fechaEntrenamiento).exists():
          AsistenciaEventoDeportivo.objects.create(fecha= fechaEntrenamiento, jugador= jug, evento=eve,justifica ='S', asiste="N")
        else:
          asist = AsistenciaEventoDeportivo.objects.get(jugador= jug, fecha = fechaEntrenamiento)
          asist.asiste ="N"
          asist.justifica="S"
          asist.evento = eve
          asist.save()

  return listarAsistencia(request)
