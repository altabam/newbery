from django import forms
from django.contrib.auth.models import User

from .models import Personas, Disciplinas, Categorias, Jugadores, Socios,IntegrantesClub,CalidadIntegrante

class PersonaForm(forms.ModelForm):
    email = forms.CharField(max_length=254)
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
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Ingrese el nombre de la nueva disciplina'}),
               }
        
class CategoriasForm(forms.ModelForm):
    class Meta:
        model=Categorias
        fields= '__all__'

class JugadoresCategoriasForm(forms.ModelForm):
    disciplina = forms.ModelChoiceField(queryset=Disciplinas.objects.all(), required=True)
    categoria = forms.ModelChoiceField(queryset=Categorias.objects.none(), required=True)
   
    persona = forms.ModelChoiceField(
        queryset=Personas.objects.all(),
        widget=forms.Select(attrs={'class': 'select2'}),
        label='Persona'
    )
    
    class Meta:
        model= Jugadores
        fields= ['persona', 'disciplina', 'categoria', 'fecha_desde']
        widgets= {'fecha_desde':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),'fecha_hasta':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
         }
        input_formats= {'fecha_desde':["%Y-%m-%d"],'fecha_hasta':["%Y-%m-%d"]
         }

    # Personalizamos la inicialización del formulario, para que solo muestre las categorías relevantes según la disciplina seleccionada
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'disciplina' in self.data:
            try:
                disciplina_id = int(self.data.get('disciplina'))
                self.fields['categoria'].queryset = Categorias.objects.filter(disciplina_id=disciplina_id).order_by('nombre')
            except (ValueError, TypeError):
                pass  
        elif self.instance.pk:
            if self.instance.categoria:
                self.fields['categoria'].queryset = Categorias.objects.filter(disciplina=self.instance.categoria.disciplina).order_by('nombre') 
    
class borrarJugadorForm(forms.ModelForm):
    class Meta:
        model =Jugadores
        fields= ['fecha_hasta']
        widgets= {'fecha_hasta':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        
         }
        input_formats= {'fecha_hasta':["%Y-%m-%d"],
         }
        
class SociosForm(forms.ModelForm):
    class Meta:
        model= Socios
        fields= '__all__'
        

class IntegranteClubForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True), required=True)
    calidad = forms.ModelChoiceField(queryset=CalidadIntegrante.objects.all(), required=True)
    class Meta:
        model= IntegrantesClub
        fields= ['user', 'calidad', 'fecha_desde', 'fecha_hasta']
        widgets= {'fecha_desde':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),'fecha_hasta':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"})
         }
        input_formats= {'fecha_desde':["%Y-%m-%d"],'fecha_hasta':["%Y-%m-%d"]
         }
