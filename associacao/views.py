from django.shortcuts import render
from sistema_tickets.models import Ticket
from servicos_produtos.models import Anuncio

def home(request):
    ultimos_tickets = Ticket.objects.all().order_by('-data_criacao')[:5]
    ultimos_anuncios = Anuncio.objects.filter(disponivel=True).order_by('-data_criacao')[:5]
    
    context = {
        'ultimos_tickets': ultimos_tickets,
        'ultimos_anuncios': ultimos_anuncios,
    }
    return render(request, 'home.html', context) 