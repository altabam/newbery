from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseBadRequest
from django.core import serializers
from django.db.models import Count
from configuracion.models import Jugadores, Categorias, Disciplinas

def reportes(request):
    return render(request, "reportes.html" )

def reporteJugadoresPorCategoria(request):
     jugxcat = Jugadores.objects.values('categoria').annotate(dcount=Count('categoria')).order_by()
     reporteJugPorCat =[]

     for categoria in jugxcat:
        print(categoria)
        cat = Categorias.objects.get(id=int(categoria['categoria']))
        dis = Disciplinas.objects.get(id= cat.disciplina.id)
        print (dis, cat)
        reporteJugPorCat.append({"disciplina":dis.nombre, "categoria":cat.nombre, "cantidad":categoria['dcount'],})
    
     print(reporteJugPorCat)

     contexto =  { "cat" : reporteJugPorCat,
    
     }
    
     print (contexto)
     return render(request, "reporteJugadoresPorCategoria.html", contexto )

def reporteJugadoresPorDisciplina(request):
     jugxdis = Jugadores.objects.values('categoria__disciplina').annotate(dcount=Count('persona', distinct=True)).order_by()
     reporteJugPorDis =[]

     for disciplina in jugxdis:
        print(disciplina)
        dis = Disciplinas.objects.get(id= int(disciplina['categoria__disciplina']))
        print (dis)
        reporteJugPorDis.append({"disciplina":dis,  "cantidad":disciplina['dcount'],})
    
     print(reporteJugPorDis)

     contexto =  { "dis" : reporteJugPorDis,
    
     }
     print (contexto)
     return render(request, "reporteJugadoresPorDisciplina.html", contexto )