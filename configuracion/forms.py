from django import forms
from .models import Personas, Disciplinas, Categorias, Jugadores

class PersonaForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = '__all__'
        widgets= {'fecha_nacimiento':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        
         }
        input_formats= {'fecha_nacimiento':["%Y-%m-%d"],
         }

class DisciplinasForm(forms.ModelForm):
    class Meta:
        model =Disciplinas
        fields= '__all__'
        
class CategoriasForm(forms.ModelForm):
    class Meta:
        model=Categorias
        fields= '__all__'

class JugadoresCategoriasForm(forms.ModelForm):
    disciplina = forms.ModelChoiceField(queryset=Disciplinas.objects.all(), required=True)
    categoria = forms.ModelChoiceField(queryset=Categorias.objects.none(), required=True)
    persona = forms.ModelChoiceField(queryset=Personas.objects.all(), required=True)  # borrar posiblemente
    class Meta:
        model= Jugadores
        fields= ['persona', 'disciplina', 'categoria', 'fecha_desde', 'fecha_hasta']
        widgets= {'fecha_desde':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),'fecha_hasta':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
         }
        input_formats= {'fecha_desde':["%Y-%m-%d"],'fecha_hasta':["%Y-%m-%d"]
         }

    