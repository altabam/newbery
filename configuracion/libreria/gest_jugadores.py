from django.http import HttpResponse
from django.shortcuts import render,redirect,get_object_or_404

from io import BytesIO # nos ayuda a convertir un html en pdf
from django.http import HttpResponse
from django.template.loader import get_template
from django.views.generic import View

from xhtml2pdf import pisa

from configuracion.models import Jugadores, Disciplinas, Categorias

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class generarPdfJugadores(View):

    def get(self, request, *args, **kwargs):
        
        print('disciplina', request.GET['disciplina'])
        print('categoria', request.GET['categoria'])
        if (request.GET['disciplina']):
          disciplinaSele = Disciplinas.objects.get(id=request.GET['disciplina'])
          if (request.GET['categoria']):
            categoriaSele = Categorias.objects.get(id= request.GET['categoria'])
            jugadores = Jugadores.objects.filter(categoria = categoriaSele)
            categoriaSele = categoriaSele.nombre
          else:
            cat = Categorias.objects.filter(disciplina = disciplinaSele)
            jugadores = Jugadores.objects.filter(categoria__in = cat)
            categoriaSele = 'todas'
        else:
           disciplinaSele='todos'
           categoriaSele = 'todas'
           jugadores = Jugadores.objects.all()
        print(jugadores)
        data = {
            'PDF':1,
            'cantidad': jugadores.count(),
            'listadoJugadores': jugadores,
            'disciplinaSele' : disciplinaSele,
            'categoriaSele': categoriaSele,
        }
        pdf = render_to_pdf('jugadores.html', data)
        print ("genera pdf",pdf)
        return HttpResponse(pdf, content_type='application/pdf')

