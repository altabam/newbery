from django.shortcuts import render,redirect
import csv
from datetime import datetime

from  configuracion.models import BecasMotivos, CalidadIntegrante, Cuotas

def cargaInicialCuotas(request):
    template_name = "configuracion/migrations/cuotas.csv"
    model = Cuotas()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            if  not Cuotas.objects.filter(concepto = row[0]).exists():
              model.id = Cuotas.objects.last().id+1
              model.concepto =row[0]
              model.valor=row[1]
              model.cant_int=row[2]
              model.save(force_insert=True)
            else:
                print(row)
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje,                  "menu": ObtenerMenu(request.user), 
    } 
    return render (request, "cargaInicial.html",contexto)

def cargaInicialMotivosBeca(request):
    template_name = "configuracion/migrations/becasMotivos.csv"
    model = BecasMotivos()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            if  not BecasMotivos.objects.filter(concepto = row[0]).exists():
              if BecasMotivos.objects.last():
                  model.id = BecasMotivos.objects.last().id+1
              else:
                  model.id = 1
              model.concepto =row[0]
              model.save(force_insert=True)
            else:
                print(row)
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje,                  "menu": ObtenerMenu(request.user), 
    } 
    return render (request, "cargaInicial.html",contexto)


def cargaInicialCalidadIntegrante(request):
    template_name = "configuracion/migrations/calidadIntegrantes.csv"
    model = CalidadIntegrante()
    with open (template_name) as f:
        reader = csv.reader(f )
        for row in reader:
            if  not CalidadIntegrante.objects.filter(concepto = row[0]).exists():
              if CalidadIntegrante.objects.last():
                 model.id = CalidadIntegrante.objects.last().id+1
              else:
                  model.id = 1

              model.concepto =row[0]
              model.save(force_insert=True)
            else:
                print(row)
    mensaje ="carga con exito"
    contexto ={  "mensaje":mensaje ,                  "menu": ObtenerMenu(request.user), 
    } 
    return render (request, "cargaInicial.html",contexto)
