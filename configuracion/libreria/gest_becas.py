from django.shortcuts import render

from datetime import datetime

from  configuracion.models import Personas, BecasJugador

def listarBecados(request):
    listarBecados = BecasJugador.objects.all()
    contexto =  { "listarBecados": listarBecados,
                  "menu": ObtenerMenu(request.user), 

    }
    print(listarBecados)
    return render(request, "listarBecados.html", contexto )

