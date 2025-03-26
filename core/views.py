from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from sistema_tickets.models import Ticket
from blog.models import Post
from atas.models import Ata
from servicos_produtos.models import Anuncio, Avaliacao
from .forms import UserRegistrationForm, UserProfileForm

@login_required
def home(request):
    context = {}
    
    # Tickets recentes do usuário
    context['tickets_recentes'] = Ticket.objects.filter(
        autor=request.user
    ).order_by('-data_criacao')[:5]
    
    # Posts recentes do blog
    context['posts_recentes'] = Post.objects.filter(
        status='publicado'
    ).order_by('-data_publicacao')[:5]
    
    # Atas recentes
    context['atas_recentes'] = Ata.objects.filter(
        publicado=True
    ).order_by('-data_reuniao')[:5]
    
    # Anúncios recentes
    context['anuncios_recentes'] = Anuncio.objects.filter(
        ativo=True
    ).order_by('-data_criacao')[:5]
    
    return render(request, 'core/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    # Estatísticas de tickets
    total_tickets = Ticket.objects.filter(autor=request.user).count()
    tickets_abertos = Ticket.objects.filter(autor=request.user, status='aberto').count()
    tickets_fechados = Ticket.objects.filter(autor=request.user, status='fechado').count()
    
    # Estatísticas de anúncios
    total_anuncios = Anuncio.objects.filter(criador=request.user).count()
    anuncios_ativos = Anuncio.objects.filter(criador=request.user).count()  # Todos os anúncios são considerados ativos
    total_avaliacoes = Avaliacao.objects.filter(anuncio__criador=request.user).count()
    
    # Atividades recentes
    tickets_recentes = Ticket.objects.filter(autor=request.user).order_by('-data_criacao')[:5]
    anuncios_recentes = Anuncio.objects.filter(criador=request.user).order_by('-data_criacao')[:5]
    
    # Combinar e ordenar atividades
    atividades_recentes = []
    for ticket in tickets_recentes:
        atividades_recentes.append({
            'titulo': ticket.titulo,
            'descricao': ticket.descricao[:100] + '...' if len(ticket.descricao) > 100 else ticket.descricao,
            'data': ticket.data_criacao,
            'tipo': f'Ticket - {ticket.get_status_display()}'
        })
    
    for anuncio in anuncios_recentes:
        atividades_recentes.append({
            'titulo': anuncio.titulo,
            'descricao': anuncio.descricao[:100] + '...' if len(anuncio.descricao) > 100 else anuncio.descricao,
            'data': anuncio.data_criacao,
            'tipo': f'Anúncio - {anuncio.get_tipo_display()}'
        })
    
    # Ordenar por data
    atividades_recentes.sort(key=lambda x: x['data'], reverse=True)
    atividades_recentes = atividades_recentes[:10]  # Limitar a 10 atividades
    
    context = {
        'total_tickets': total_tickets,
        'tickets_abertos': tickets_abertos,
        'tickets_fechados': tickets_fechados,
        'total_anuncios': total_anuncios,
        'anuncios_ativos': anuncios_ativos,
        'total_avaliacoes': total_avaliacoes,
        'atividades_recentes': atividades_recentes,
    }
    
    return render(request, 'registration/profile.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'registration/register.html', {'form': form}) 