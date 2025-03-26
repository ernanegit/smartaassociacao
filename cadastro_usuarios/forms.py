from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PerfilMorador

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

class PerfilForm(forms.ModelForm):
    class Meta:
        model = PerfilMorador
        fields = ['cpf', 'telefone', 'endereco', 'numero_casa', 'data_nascimento', 'foto_perfil']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        } 