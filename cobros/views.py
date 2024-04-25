from django.shortcuts import render, redirect
from django.template import context, Template


# Create your views here.

def render_cobros(request):
    
    return render(request, "cobros.html", )
    

