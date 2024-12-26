import os
from django.shortcuts import render
from django.db import connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from administracion.models import ValidacionEmail

# Create your views here.
def actualizarSecuenciaIdPersonas(request):
    with connection.cursor() as cursor:
      cursor.execute("SELECT setval(pg_get_serial_sequence('""configuracion_personas""','id'), coalesce(max('id'), 1), max('id') IS NOT null) FROM 'configuracion_personas';")
    return render(request,'configuracion/cargaMasiva.html', contexto)   


def existeEmail(mail):
  retorno = False
  print (mail)
  user = User.objects.filter(email=mail)
  if (user):
    print(user)
    retorno= True

  
  return retorno

def enviarEmail(request):
  if(existeEmail(request.POST.get('email'))):
    
    # Renderizar la plantilla
    url_app = "https://"+ os.getenv('URL_APP')+"/administracion/mailValidador"
    print(url_app)
    mensaje = '<h1>Hola Marcelo</h1> <p>Gracias por registrarte en nuestro sitio.</p> '
    # Enviar el correo
    email = EmailMessage(
      subject='Bienvenido a nuestro sitio',
      body=mensaje,
      from_email='altabam@gmail.com',
      to=['altabam@yahoo.com.ar'],
    )
    email.content_subtype = 'html'  # Define el tipo como HTML
    #email.send()
    contexto = { "mensajeEnvio":"El mail fue enviado correctametne",}
  else:
   print   ("entro en el else")
   contexto = { "mensajeEnvio":"El mail no se pudo enviar, porque no corresponde con ningun usuario",}
  return render(request, 'envioEmail.html', contexto)   

def envioEmail(request):
  contexto = {}
  return render(request, 'envioEmail.html', contexto)   


