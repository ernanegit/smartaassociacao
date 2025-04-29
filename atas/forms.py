# atas/forms.py
from django import forms
from .models import Ata

class AtaForm(forms.ModelForm):
    class Meta:
        model = Ata
        fields = ['titulo', 'descricao', 'arquivo', 'data_reuniao', 'categoria', 'destaque']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control'}),
            'data_reuniao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'destaque': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }