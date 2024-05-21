from datetime import datetime

from  configuracion.models import Personas

def cargarPersona(row):
    model = Personas()
    print("nombre:"+ row[2])
    print("fecha_nac:"+ row[3])
    if Personas.objects.last():
        model.id = Personas.objects.last().id+1
    else:
        model.id = 1
    model.dni=row[0]
    model.apellido=row[1]
    model.nombre =row[2]
    if row[3] != "":
        model.fecha_nacimiento=datetime.strptime(row[3], '%d/%m/%Y').date()
    model.telefono=row[4]
    model.direccion=row[5]
    model.save(force_insert=True)