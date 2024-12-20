from django.shortcuts import render
from django.db import connection
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.
def actualizarSecuenciaIdPersonas(request):
    with connection.cursor() as cursor:
      cursor.execute("SELECT setval(pg_get_serial_sequence('""configuracion_personas""','id'), coalesce(max('id'), 1), max('id') IS NOT null) FROM 'configuracion_personas';")
    return render(request,'configuracion/cargaMasiva.html', contexto)   

def enviarEmail(request):
 # Renderizar la plantilla
  mensaje = '<h1>Hola Marcelo</h1> <p>Gracias por registrarte en nuestro sitio.</p>'
  # Enviar el correo
  email = EmailMessage(
    subject='Bienvenido a nuestro sitio',
    body=mensaje,
    from_email='altabam@gmail.com',
    to=['altabam@yahoo.com.ar'],
  )
  email.content_subtype = 'html'  # Define el tipo como HTML
  email.send()

def envioEmail(request):
  contexto = {}
  return render(request, 'envioEmail.html', contexto)   

