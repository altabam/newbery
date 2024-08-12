from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date

from configuracion.models import Socios, BecasJugador, Jugadores,Cuotas
from .models import DetallePagos , Pagos, SituacionInicial
from .forms import CobrosCreationForm, SituacionInicialForm

# Create your views here.

    


def render_cobros(request):
    
    return render(request, "cobros.html", )

def pagarCuota(request):
    return render(request, "pagarCuota.html")

def verPagoSocio(request,id):
    meses =[  "ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL","AGO","SEP", "OCT", "NOV","DIC", ]
    anio_actual = date.today().year
    mes_actual = int(date.today().month)
    becados =[]
    print (mes_actual)
    anio_anterior =  str(int(anio_actual)-1)
    anios = [anio_anterior, anio_actual]
    socio = Socios.objects.get(id=id)
    socios = Socios.objects.filter(numero = socio.numero)
    montoDisciplina = Cuotas.objects.get(cant_int=1, fecha_hasta = None)
    print(socios)
    cantIntegrantes=0
    montoBeca =0
    for beca in socios:
         cantIntegrantes=cantIntegrantes+1
         print(beca.persona)
         if Jugadores.objects.filter(persona = beca.persona).exists():
            jugador = Jugadores.objects.get(persona = beca.persona)
            print("jugador:",jugador)
            if BecasJugador.objects.filter(jugador = jugador).exists():
                integrante = BecasJugador.objects.get(jugador  = jugador)
                becados.append(integrante)
                montoBeca = montoBeca+ float(montoDisciplina.valor)*float( integrante.beca.porcentaje)
    print("cantidad de integrantes:"+ str(cantIntegrantes))
    montoCuota =  float(Cuotas.objects.get(cant_int = cantIntegrantes, fecha_hasta = None).valor) - float(montoBeca)
    print (montoCuota)
    montoDebe = 0
    mes =1
    pagos=[]
    mesesCab=[]
    if request.method == 'POST':
        form = CobrosCreationForm(request.POST)
        if form.is_valid():
            model = Pagos()
            model.socio = socio
            model.fecha_pago = datetime.today()
            model.monto = float(form.data.get('cantCuotas'))*montoCuota
            model.save(force_insert=True)
            grabarDetallePago(model, int( form.data.get('cantCuotas')))
            print("pasa por aqui")
            for listado in DetallePagos.objects.all():
                print (listado.anio, listado.mes, listado.pago.socio.persona.apellido)

    else:
        form = CobrosCreationForm()
    

    pagoSocio = Pagos.objects.filter(socio= socio)
    for i in anios:
        mesesAnioPago=[]
        mes = 1
        for j in meses:
            if i == anio_actual and mes > mes_actual:
                print("no va este mes")
            else:
                  #  print("va este mes:",j)
                    detallePago = DetallePagos.objects.filter(anio=i, mes=mes, pago__in = pagoSocio)

                    if (detallePago):
                        mesesAnioPago.append("P")
                    else:
                        mesesAnioPago.append("Debe")
                        montoDebe = montoDebe + montoCuota
                    mesesCab.append(j)
            mes= mes +1
        #print (mesesCab)
        pagos.append({"anio":i,"cabMeses":mesesCab,'pagoMeses': mesesAnioPago})
        mesesCab=[]
        #print("meses: ", mesesCab, "anio:", i)
    listadoCobros = pagoSocio
    print("ver listado de cobros")
    print(listadoCobros)           
    
    contexto =  { "listadoSocios": socios,
                 "listadoPagos":pagos,
                 "montoBeca" : montoBeca,
                 "montoCuota" : montoCuota,
                 "montoDebe" : montoDebe,
                 "listabecados" : becados,
                 "listadoCobros" : listadoCobros,
                 "form": form,
    }
    return render(request, "verPagoSocio.html", contexto )


def  grabarDetallePago(pago, cantCuotas):
    pagoSocio = Pagos.objects.filter(socio = pago.socio)
    detallePago = DetallePagos.objects.filter(pago__in = pagoSocio).last()
    print ("ultimpo pago")
    print(detallePago)
    if not detallePago:
        anio = date.today().year -1
        mes = 1
    else: 
        anio = int(detallePago.anio)
        mes = int(detallePago.mes) + 1

    print(detallePago)
    for recorrer in range(mes , mes+cantCuotas):
        if recorrer >12:
            cuota = recorrer-12
            if cuota == 1:
                anio = anio+1

        else:
            cuota = recorrer
        print("grabar detalle de pagos")
        print(anio, pago, cuota)
        model = DetallePagos()
        model.anio = anio
        model.pago = pago
        model.mes = cuota
        model.save(force_insert=True)


def agregarSitInicial(request):
    if request.method == 'POST':
        form= SituacionInicialForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('/cobros/listarSitInicial')
    else:
        form =SituacionInicialForm()

    contexto ={ 
            "accion":"Agregar", 
            "form": form,
         } 
    return render(request, "editarSituacionInicial.html", contexto )    

def editarSitInicial(request,id):
    sitInicial = SituacionInicial.objects.get(id = id)
    if request.method == 'POST':
        form= SituacionInicialForm(request.POST, instance=sitInicial)
        if form.is_valid():
            form.save()
            return redirect('/cobros/listarSitInicial')
    else:
            form = SituacionInicialForm( instance=sitInicial)
    
    contexto ={ 
            "accion":"Modificar", 
            "form": form,
            "datos": sitInicial,
         } 
    return render(request, "editarSituacionInicial.html",contexto)

def listarSitInicial(request):
    listadoSitInicial = SituacionInicial.objects.all()
    contexto = { "listadoSitInicial": listadoSitInicial }
    return render(request, "situacioninicial.html",  contexto)

def borrarSitInicial(request, id):
    SituacionInicial.objects.filter(id=id).delete()
    listadoSitInicial = SituacionInicial.objects.all()
    contexto = { "listadoSitInicial": listadoSitInicial }
    return render(request, "situacioninicial.html",  contexto)

def listarSociosDeuda(request):
    socios = Socios.objects.filter(responsable='S')
    listadoDeudores=[]
    montoTotalDeuda =0
    for socio in socios :
         
        cuotasImpagas =  calcularCuotasImpagas(socio)
        if cuotasImpagas > 0:
            montos = calcularMontoPago(socio.numero)
            deuda = montos['montoPagar'] * cuotasImpagas
            listadoDeudores.append({
                "numero":socio.numero,
                "dni":socio.persona.dni, 
                "nombre":socio.persona.nombre+" "+ socio.persona.apellido, 
                "montoDeuda": deuda,
                "montoCuota": montos['montoCuota'],
                "montoBeca" : montos['montoBeca'],
                "montoPagar": montos['montoPagar'],
                "cuotasImpagas" : cuotasImpagas
            })
            montoTotalDeuda += deuda

    
    contexto = { "listadoDeudores": listadoDeudores,
                 "montoTotalDeuda": montoTotalDeuda}
    return render(request, "listadoDeudores.html",  contexto)

def calcularMontoPago(nroSocio):
    integrantes = Socios.objects.filter(numero = nroSocio)
    cantIntegrantes = 1
    montoCuota  = Cuotas.objects.get(cant_int=1, fecha_hasta=None).valor
    montoBeca =0
    for integrante in integrantes:
         if Jugadores.objects.filter(persona = integrante.persona).exists():
            disciplinasParticipa = Jugadores.objects.filter(persona = integrante.persona)
            for jugador in disciplinasParticipa:
                if (jugador.fecha_hasta is None):
                    if (jugador.categoria.paga_disciplina):
                        cantIntegrantes=cantIntegrantes+1
                        if BecasJugador.objects.filter(jugador = jugador).exists():
                            integrante = BecasJugador.objects.get(jugador  = jugador)
                            montoBeca = montoBeca+ float(montoCuota)*float( integrante.beca.porcentaje)
    montoCuota =  float(Cuotas.objects.get(cant_int = cantIntegrantes, fecha_hasta=None).valor) 
    montoPagar = montoCuota - float(montoBeca)
    montos ={"montoBeca": montoBeca, "montoCuota": montoCuota,"montoPagar": montoPagar}
    return montos

def calcularCuotasImpagas(socio):
    meses =[  "ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL","AGO","SEP", "OCT", "NOV","DIC", ]
    anio_actual = date.today().year
    mes_actual = int(date.today().month)
    anio_anterior =  str(int(anio_actual)-1)
    anios = [anio_anterior, anio_actual]
    cantCuotasImpagas = 0
    pagoSocio = Pagos.objects.filter(socio= socio)
    for i in anios:
        mes = 1
        for j in meses:
            if not (i == anio_actual and mes > mes_actual):
                detallePago = DetallePagos.objects.filter(anio=i, mes=mes, pago__in = pagoSocio)
                if (not detallePago):
                    cantCuotasImpagas +=1
            mes= mes +1
    return cantCuotasImpagas


