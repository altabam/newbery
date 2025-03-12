from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.db.models import Count, Subquery
from datetime import date
import calendar
from django.core.exceptions import ObjectDoesNotExist   
from .models import AsistenciaEventoDeportivo, CaracteristicaEvaluar, EvalTecnicoTacticaActitudinalJugador, EvalTecnicoTacticaActitudinal,EvalTecnicoTacticaActitudinalCaracteristica

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
     # print (jug)
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


def listarEvaluacionTTA(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    eventosDep = EventoDeportivo.objects.all()

    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Asistencia de Jugadores",
                 "anio": date.today().year,
                 "mes" : date.today().month,
                 "categoriaSele": 0,
               }
    return filtrarEvaluacionTTAJugadoresCategoria(request, date.today().year, 0, 0)


def filtrarEvaluacionTTAJugadoresCategoria(request, anio, accion, categoria ):
    #accion 0-mantener mes  1-incrementar mes   2-decrementar mes
    #anio = date.today().year
    #mes = date.today().month
    if request.GET:
       if request.GET["categoria"]=="":
         categoriaSele =0
       else:      
         categoriaSele = request.GET["categoria"]
    else:
       categoriaSele = int(categoria)

    intClub = IntegrantesClub.objects.filter(user= request.user)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    if (categoriaSele == 0):
      cat = []
      for icc in intClubCat:
        cat.append(  icc.categorias)
      jugadores = Jugadores.objects.filter(categoria__in = cat)
    else:
      jugadores = Jugadores.objects.filter(categoria = categoriaSele)

    matrizAsistencia= []
    matrizJugador= []
    if (accion==2):
          anio -=1
    elif(accion==1):
          anio +=1
    caracteristicaEvaluar = EvalTecnicoTacticaActitudinal.objects.filter(anio = anio)
    for carEvaluar in caracteristicaEvaluar:
      datosEvaluacion = []
      if carEvaluar.fechaInicio <= date.today() and carEvaluar.fechaFin >= date.today():
        datosEvaluacion.append(0)
        datosEvaluacion.append(carEvaluar.pk)
        datosEvaluacion.append(carEvaluar.mes)
      else:
       # print("fechas", carEvaluar.fechaInicio, carEvaluar.fechaFin, date.today())
        datosEvaluacion.append(1)
        datosEvaluacion.append(carEvaluar.pk)
        datosEvaluacion.append(carEvaluar.mes)
      matrizJugador.append(datosEvaluacion)
    matrizAsistencia.append(matrizJugador)
    print(matrizJugador)
    matrizJugador=[]
   # print("matriz inicial", matrizJugador, matrizAsistencia)
    for jug in jugadores:
      matrizJugador.append(jug.persona.apellido+" "+jug.persona.nombre)
      for evalJugador in caracteristicaEvaluar:
          datosEvaluacion= []       
      #    print(evalJugador.fechaInicio, evalJugador.fechaFin)           
          if evalJugador.fechaFin >= date.today() and evalJugador.fechaInicio <= date.today():
              datosEvaluacion.append(0)
          else: 
              datosEvaluacion.append(1)
             # print("fechas", evalJugador.fechaInicio, evalJugador.fechaFin, date.today())

          caracteristica = EvalTecnicoTacticaActitudinalCaracteristica.objects.filter(tipoEvaluacion = evalJugador).last()
          caracteristicaJugador = EvalTecnicoTacticaActitudinalJugador.objects.filter(caracteristicaEvaluar = caracteristica,jugador = jug)
          if caracteristicaJugador.exists():
             datosEvaluacion.append(jug.pk)
             datosEvaluacion.append(evalJugador.pk)
             datosEvaluacion.append("realizada")
          else:             
             datosEvaluacion.append(jug.pk)
             datosEvaluacion.append(evalJugador.pk)
             datosEvaluacion.append("Sin realizar")
          matrizJugador.append(datosEvaluacion)
      matrizAsistencia.append(matrizJugador)
      #print(matrizJugador)
      matrizJugador=[]
        
    cantElemFila= len(matrizAsistencia[0])
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Evaluacion Tec. Tac. Act.",
                 "anio": anio,
                 "cantElemFila":cantElemFila,
                 "matrizAsistencia" :matrizAsistencia,
                 "categoriaSele": categoriaSele,
                 "anioHoy": date.today().year,
               }
    return render(request, "listarEvaluacionTTA.html",  contexto)

def obtenerHabilidadesEvaluar(jugador, evaluacion):
   habilidadesEvaluar =[]
   caracteristicaEval = EvalTecnicoTacticaActitudinalCaracteristica.objects.filter(tipoEvaluacion_id = evaluacion)
   if EvalTecnicoTacticaActitudinalJugador.objects.filter(caracteristicaEvaluar__in =caracteristicaEval, jugador= jugador ).exists():
      evalTecnicoTacticaActitudinalJugador = EvalTecnicoTacticaActitudinalJugador.objects.filter(caracteristicaEvaluar__in =caracteristicaEval, jugador= jugador )
      print("evalTecnicoTacticaActitudinalJugador",evalTecnicoTacticaActitudinalJugador)
      for ettaj in evalTecnicoTacticaActitudinalJugador:
        celda = []
        celda.append(ettaj)
        celda.append(ettaj.evaluacion)
        habilidadesEvaluar.append(celda)
        #print("ettaj:", ettaj)
   else:
      #print("habilidadesEvaluar",habilidadesEvaluar)
      for ettac in caracteristicaEval:
        celda = []
        celda.append(ettac)
        celda.append('')
        habilidadesEvaluar.append(celda)
        #print("ettac:", ettac)
   #print("habilidades:",habilidadesEvaluar)
      
   return habilidadesEvaluar

def cargarEvaluacionTTAJugadoresCategoria(request, jugador, evaluacion, categoria, anio):
  print(request.POST)
 # print("pasa por aqui")
 # print(jugador, evaluacion)
  intClub = IntegrantesClub.objects.filter(user= request.user)
  intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
  evaluacionSele = EvalTecnicoTacticaActitudinal.objects.get(id = evaluacion)
  caracteristicaEvalRaiz = CaracteristicaEvaluar.objects.filter(caracteristicaPadre__isnull = True)
  matrizEvaluacion=[]
  columna1=[]
  columna2=[]
  datoFila1=[]
  datoFila2=[]
  datoFila1.append(0)
  datoFila1.append(1)
  columna1.append(datoFila1)
  datoFila2.append(0)
  datoFila2.append(1)
  columna2.append(datoFila2)
  for cabecera in caracteristicaEvalRaiz:
    contador = 0
    datoFila1 =[]
    datoFila1.append(cabecera.caracteristica)
    cab2Niv = CaracteristicaEvaluar.objects.filter(caracteristicaPadre = cabecera.id)
    for cab2 in cab2Niv:
       datoFila2 =[]
       contador = contador+1
       datoFila2.append(cab2.caracteristica)
       datoFila2.append(1)
       columna2.append(datoFila2)
    datoFila1.append(contador)
    columna1.append(datoFila1)
  matrizEvaluacion.append(columna1)
  matrizEvaluacion.append(columna2)
     
#  matrizEvaluacion.append(columna)
  
  print(" matrizEvaluacion)",matrizEvaluacion)
  #print("eva:", evaluacionSele)
  if (jugador==0):
#     print("selecciono 0 y pasa por todos los jugadores")
     jugadores = Jugadores.objects.filter(categoria = categoria)
  else:
#    print ("jugador:", jugador)
    jugadores = Jugadores.objects.filter(id= jugador)
#    print ("jugador:", jugadores)

  for jug in jugadores:
    columna1 =[]
    columna1.append(jug.pk)
    columna1.append(jug.persona.apellido+" "+ jug.persona.nombre)
    habilidadesEvaluar = obtenerHabilidadesEvaluar(jug,evaluacionSele)
    for habEva in habilidadesEvaluar:
       columna1.append(habEva[1])
    print(columna1)
    matrizEvaluacion.append(columna1)

    valoresEvaluacionTTA=  (
        ("A", "Alto 10 a 8"),
        ("M", "Medio 7 a 5"),
        ("B", "Bajo 4 a 1"),
        ("N", "No Evaluado"),
    )
  #print(valoresEvaluacionTTA)
  contexto = { 
               "menu": ObtenerMenu(request.user), 
               "titulo": "Cargar Evaluacion",
               "categoriaSele": categoria,
               "anioSele": anio,
               "evaluacionSele":evaluacionSele,
               "matrizEvaluacion" :matrizEvaluacion,
               "valoresEvaluacionTTA" : valoresEvaluacionTTA,
               "boton_texto": "Guardar Evaluacion",
               "evaluacionSele": evaluacion
             }

  return render(request,"cargarEvaluacionTTAJugador.html", contexto)

def guardarEvaluacionTTAJugadoresCategoria(request,evaluacion):
   #print("pasa por guardarEvaluacionTTAJugadoresCategoria")
   #print(request.POST)
   intClub = IntegrantesClub.objects.get(user= request.user)
   intClubCat = IntegrantesClubCategorias.objects.filter(integrante= intClub)
   #print(intClubCat)

   eval = EvalTecnicoTacticaActitudinal.objects.get(id = evaluacion)
   caracteristicaEvaluar = EvalTecnicoTacticaActitudinalCaracteristica.objects.filter(tipoEvaluacion= eval)
   #print(caracteristicaEvaluar)
   valorEvaluacion = request.POST.getlist('evalTTA')
   #print(valorEvaluacion)
   jugador = Jugadores.objects.filter(id= request.POST['jugador'])
   indice = 0
   for jug in jugador:
     categoria = jug.categoria
     for carEval in caracteristicaEvaluar:
       if EvalTecnicoTacticaActitudinalJugador.objects.filter(jugador = jug, caracteristicaEvaluar = carEval).exists():
    #    print   ("existe : ", valorEvaluacion[indice])
        evalTTAJugador = EvalTecnicoTacticaActitudinalJugador.objects.get(jugador = jug, caracteristicaEvaluar = carEval)
        evalTTAJugador.evaluacion = valorEvaluacion[indice]
        evalTTAJugador.fecha = date.today()
        evalTTAJugador.evaluador = intClub
        indice= indice+1   
       else:
      #  print   ("No existe : ", valorEvaluacion[indice])
        EvalTecnicoTacticaActitudinalJugador.objects.create(jugador=jug, caracteristicaEvaluar = carEval, evaluacion= valorEvaluacion[indice], fecha= date.today(), evaluador=intClub,observaciones='' )
        indice= indice+1   
        
   
      
   return filtrarEvaluacionTTAJugadoresCategoria(request, eval.anio, 0, categoria.pk  )

