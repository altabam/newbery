from configuracion.models import Personas

def prueba():
    persona = Personas.objects.get(id=1)
    print(persona.apellido)