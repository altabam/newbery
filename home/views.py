from django.shortcuts import render

# Create your views here.
def render_home(request):
    return render(request, "index.html")

def tablasParametricas(request):
    return render(request, "tablasParametricas.html")

def listados(request):
    return render(request, "listados.html")
