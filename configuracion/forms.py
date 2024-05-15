from django import forms
from .models import Personas
class PersonaForm(forms.ModelForm):
    class Meta:
        model = Personas
        fields = '__all__'
