from django import forms
from .models import Personas
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = '__all__'
        widgets= {'fecha_nacimiento':forms.DateInput(format="%Y-%m-%d", attrs={"type": "date"}),
        
         }
        input_formats= {'fecha_nacimiento':["%Y-%m-%d"],
         }
