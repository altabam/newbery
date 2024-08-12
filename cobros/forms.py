from django import forms

from .models import Pagos, DetallePagos, SituacionInicial



class CobrosCreationForm(forms.Form):
    cantCuotas = forms.CharField(max_length=30)

    def retornarDato():
        return cantCuotas()


class SituacionInicialForm(forms.ModelForm):
    class Meta:
        model = SituacionInicial
        fields = '__all__'
