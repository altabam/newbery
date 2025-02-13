
from django.shortcuts import render,redirect
from django.templatetags.static import static
from django.contrib.auth.models import User
from configuracion.models import IntegrantesClub, CalidadIntegrante
from configuracion.forms import IntegranteClubForm, CalidadIntegrante
from home.views import ObtenerMenu

def agregarIntegranteClub(request):
    usuario = User.objects.filter(is_active= True)
    print("agregar integra")
    print(usuario)
    calidad = CalidadIntegrante.objects.all()

    if request.method == 'POST':
        form= IntegranteClubForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/configuracion/listarIntegrantesClub')
    else:
        form= IntegranteClubForm()
    contexto = {
        'form': form,
        'titulo': 'Agregar Jugador a Categoría',
        'boton_texto': 'Agregar Jugador',
        "menu": ObtenerMenu(request.user), 
    }
    return render(request, 'agregarJugadorCategorias.html', contexto) 


def gestionarIntegranteClub(request):
    return render(request, 'agregarJugadorCategorias.html', contexto) 


def editarIntegranteClub(request):
    return render(request, 'agregarJugadorCategorias.html', contexto) 


def borrarIntegranteClub(request):
    return render(request, 'agregarJugadorCategorias.html', contexto) 
