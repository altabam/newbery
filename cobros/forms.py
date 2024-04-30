from django import forms

from .models import Cobros

class CobrosForm(forms.ModelForm):
    class Meta:
        model = Cobros
        fields = '__all__'
