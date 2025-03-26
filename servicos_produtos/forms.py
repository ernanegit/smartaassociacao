from django import forms
from .models import Anuncio, Avaliacao

class AnuncioForm(forms.ModelForm):
    class Meta:
        model = Anuncio
        fields = ['titulo', 'descricao', 'tipo', 'categoria', 'preco', 'imagem', 'contato', 'local']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'preco': forms.NumberInput(attrs={'min': '0', 'step': '0.01'}),
        }

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'comentario': forms.Textarea(attrs={'rows': 3}),
            'nota': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
        } 