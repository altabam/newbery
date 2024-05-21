from django.shortcuts import render
from datetime import datetime, timedelta, date

from configuracion.models import Socios
from .models import DetallePagos

# Create your views here.

    


def render_cobros(request):
    
    return render(request, "cobros.html", )


def verPagoSocio(request,id):
    meses =[  "ENE", "FEB", "MAR", "ABR", "MAY", "JUN", "JUL","AGO","SEP", "OCT", "NOV","DIC", ]
    anio_actual = date.today().year
    mes_actual = int(date.today().month)
    print (mes_actual)
    anio_anterior =  str(int(anio_actual)-1)
    anios = [anio_anterior, anio_actual]
    socio = Socios.objects.get(id=id)
    socios = Socios.objects.filter(numero = socio.numero)
    print(socios)
    becas = 123
    montoPago = 2700
    mes =1
    pagos=[]
    mesesCab=[]
    for i in anios:
        mesesAnioPago=[]
        mes = 1
        for j in meses:
            if i == anio_actual and mes > mes_actual:
                print("no va este mes")
            else:
                    print("va este mes:",j)
                    detallePago = DetallePagos.objects.filter(anio=i, mes=j)
                    if (detallePago):
                        mesesAnioPago.append("P")
                    else:
                        mesesAnioPago.append("Debe")
                    mesesCab.append(j)
            mes= mes +1
        print (mesesCab)
        pagos.append({"anio":i,"cabMeses":mesesCab,'pagoMeses': mesesAnioPago})
        mesesCab=[]
        print("meses: ", mesesCab, "anio:", i)
        
    
    print(pagos)           
    print("___________")
    contexto =  { "listadoSocios": socios,
                 "listadoPagos":pagos,
                 "becas" : becas,
                 "montoPago" : montoPago
    }
    return render(request, "verPagoSocio.html", contexto )
