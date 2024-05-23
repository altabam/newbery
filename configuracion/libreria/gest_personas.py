from datetime import datetime

from  configuracion.models import Personas

def cargarPersona(row):
    model = Personas()
    print("nombre:"+ row[2])
    print("fecha_nac:"+ row[3])
    id =Personas.objects.order_by(id).last().id+1
    if id:
        model.id = id
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