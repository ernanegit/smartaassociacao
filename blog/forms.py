from django import forms
from .models import Post, Comentario

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'categoria', 'conteudo', 'imagem', 'status', 'destaque']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 