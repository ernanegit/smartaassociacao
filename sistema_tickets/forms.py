from django import forms
from .models import Ticket, ComentarioTicket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['titulo', 'descricao', 'categoria', 'prioridade', 'status']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'prioridade': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if not self.user or not self.user.is_staff:
            self.fields.pop('status')

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = ComentarioTicket
        fields = ['conteudo']
        widgets = {
            'conteudo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        } 