from django.shortcuts import render
from django.http import HttpResponse
import csv

from configuracion.models import Personas


def realizarBackup(request,slug):
    response = HttpResponse(
        content_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="'+slug+'.csv"'},
    )
    writer = csv.writer(response)
    writer = backupPersonas(writer)

    return response

def backupPersonas(writer):    
    writer.writerow(["id","nombre","apellido","dni","fecha_nacimiento","telefono","direccion"])
    personas = Personas.objects.all()
    columnas = []
    for p in personas:
            columnas = [str(p.id),p.nombre,p.apellido,str(p.dni),str(p.fecha_nacimiento),p.telefono, p.direccion]
            writer.writerow(columnas)
    return writer

    