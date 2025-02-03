from django.shortcuts import render
from django.http import  HttpResponse,HttpResponseBadRequest
from django.core import serializers
from django.db.models import Count
from configuracion.models import Jugadores, Categorias, Disciplinas
from home.views import ObtenerMenu

def reportes(request):
   contexto =  {   "menu": ObtenerMenu(request.user), 

   }    
   return render(request, "reportes.html",contexto )

def reporteJugadoresPorCategoria(request):
     jugxcat = Jugadores.objects.values('categoria').annotate(dcount=Count('categoria')).order_by('categoria__disciplina')
     reporteJugPorCat =[]

     for categoria in jugxcat:
        print(categoria)
        cat = Categorias.objects.get(id=int(categoria['categoria']))
        dis = Disciplinas.objects.get(id= cat.disciplina.id)
        print (dis, cat)
        reporteJugPorCat.append({"disciplina":dis.nombre, "categoria":cat.nombre, "cantidad":categoria['dcount'],})
    
     print(reporteJugPorCat)

     contexto =  { "cat" : reporteJugPorCat,
                                    "menu": ObtenerMenu(request.user), 

    
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
                  "menu": ObtenerMenu(request.user), 
    
     }
     print (contexto)
     return render(request, "reporteJugadoresPorDisciplina.html", contexto )