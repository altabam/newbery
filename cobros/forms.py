from django import forms

from .models import Pagos, DetallePagos



class CobrosCreationForm(forms.Form):
    cantCuotas = forms.CharField(max_length=30)

    def retornarDato():
        return cantCuotas()
