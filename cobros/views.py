from django.shortcuts import render
from datetime import datetime, timedelta, date

from configuracion.models import Socios, BecasJugador, Jugadores,Cuotas
from .models import DetallePagos , Pagos
from .forms import CobrosCreationForm

# Create your views here.

    


def render_cobros(request):
    
    return render(request, "cobros.html", )


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
    montoDisciplina = Cuotas.objects.get(cant_int=1)
    print(socios)
    cantIntegrantes=0
    montoBeca =0
    for beca in socios:
         cantIntegrantes=cantIntegrantes+1
         print(beca.persona)
         if Jugadores.objects.filter(persona = beca.persona).exists():
            jugador = Jugadores.objects.get(persona = beca.persona)
            integrante = BecasJugador.objects.get(jugador  = jugador)
            if integrante:
                  becados.append(integrante)
                  montoBeca = montoBeca+ float(montoDisciplina.valor)*float( integrante.beca.porcentaje)
    print("cantidad de integrantes:"+ str(cantIntegrantes))
    montoCuota =  float(Cuotas.objects.get(cant_int = cantIntegrantes).valor) - float(montoBeca)
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


