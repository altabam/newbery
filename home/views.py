from django.shortcuts import render
from home.models import Menu, MenuGroup
from django.contrib.auth.models import Group

# Create your views here.
def render_home(request):
    print (request.user)
    if (request.user.is_authenticated ):
      contexto =   { "menu": ObtenerMenu(request.user) }
    else:
      contexto ={}
    
    return render(request, "index.html", contexto)

def tablasParametricas(request):
    return render(request, "tablasParametricas.html")

def listados(request):
    return render(request, "listados.html")

def ObtenerMenu(user):
    print(user)
    group =Group.objects.filter(user=user)
    menuUsuario = MenuGroup.objects.filter(groups__in = group)
    #menu = Menu.objects.filter(id__in = menuUsuario.menu_id)
    print(menuUsuario )
    #permisos = MenuGroup.objects.filter(groups= user.groups)
  #  print(permisos)
   # return Menu.objects.all()
    return menuUsuario
