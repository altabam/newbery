from django.shortcuts import render,redirect,get_object_or_404
from django.templatetags.static import static
from django.contrib.auth.models import User
from django.db.models import Count, Subquery
from django.core.exceptions import ObjectDoesNotExist   
from .models import AsistenciaEventoDeportivo

from home.views import ObtenerMenu
from configuracion.models import IntegrantesClub,IntegrantesClubCategorias

#from .forms import PersonaForm, DisciplinasForm, CategoriasForm, JugadoresCategoriasForm,borrarJugadorForm

# Create your views here.
def cargarAsistencia(request):
    intClub = IntegrantesClub.objects.filter(user= request.user)
    print(intClub)
    intClubCat = IntegrantesClubCategorias.objects.filter(integrante__in= intClub)
    contexto = { "categorias": intClubCat,
                 "menu": ObtenerMenu(request.user), 
                 "titulo": "Cargar Asistencia de Jugadores",
                 "boton_texto": "Cargar Asistencia",
               }
    return render(request, "cargarAsistencia.html",  contexto)
