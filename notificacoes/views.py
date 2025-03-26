from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Notificacao

# Create your views here.

@login_required
def lista_notificacoes(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user)
    nao_lidas = notificacoes.filter(lida=False).count()
    
    context = {
        'notificacoes': notificacoes,
        'nao_lidas': nao_lidas,
    }
    return render(request, 'notificacoes/lista_notificacoes.html', context)

@login_required
def detalhe_notificacao(request, slug):
    notificacao = get_object_or_404(Notificacao, slug=slug, usuario=request.user)
    
    if not notificacao.lida:
        notificacao.marcar_como_lida()
    
    return render(request, 'notificacoes/detalhe_notificacao.html', {
        'notificacao': notificacao
    })

@login_required
def marcar_como_lida(request, slug):
    notificacao = get_object_or_404(Notificacao, slug=slug, usuario=request.user)
    notificacao.marcar_como_lida()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'Notificação marcada como lida.')
    return redirect('notificacoes:lista')

@login_required
def marcar_todas_como_lidas(request):
    Notificacao.objects.filter(usuario=request.user, lida=False).update(lida=True)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, 'Todas as notificações foram marcadas como lidas.')
    return redirect('notificacoes:lista')

@login_required
def obter_contador_notificacoes(request):
    nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False).count()
    return JsonResponse({'nao_lidas': nao_lidas})
