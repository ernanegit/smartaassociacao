from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Anuncio, Avaliacao
from .forms import AnuncioForm, AvaliacaoForm

def lista_anuncios(request):
    anuncios = Anuncio.objects.all().order_by('-data_criacao')
    return render(request, 'servicos_produtos/lista_anuncios.html', {'anuncios': anuncios})

@login_required
def criar_anuncio(request):
    if request.method == 'POST':
        form = AnuncioForm(request.POST)
        if form.is_valid():
            anuncio = form.save(commit=False)
            anuncio.criador = request.user
            anuncio.save()
            messages.success(request, 'Anúncio criado com sucesso!')
            return redirect('servicos_produtos:detalhe_anuncio', pk=anuncio.pk)
    else:
        form = AnuncioForm()
    return render(request, 'servicos_produtos/criar_anuncio.html', {'form': form})

def detalhe_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    avaliacoes = anuncio.avaliacoes.all().order_by('-data_criacao')
    return render(request, 'servicos_produtos/detalhe_anuncio.html', {
        'anuncio': anuncio,
        'avaliacoes': avaliacoes
    })

@login_required
def editar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, criador=request.user)
    if request.method == 'POST':
        form = AnuncioForm(request.POST, instance=anuncio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Anúncio atualizado com sucesso!')
            return redirect('servicos_produtos:detalhe_anuncio', pk=anuncio.pk)
    else:
        form = AnuncioForm(instance=anuncio)
    return render(request, 'servicos_produtos/editar_anuncio.html', {
        'form': form,
        'anuncio': anuncio
    })

@login_required
def excluir_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, criador=request.user)
    if request.method == 'POST':
        anuncio.delete()
        messages.success(request, 'Anúncio excluído com sucesso!')
        return redirect('servicos_produtos:lista_anuncios')
    return render(request, 'servicos_produtos/excluir_anuncio.html', {'anuncio': anuncio})

@login_required
def avaliar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk)
    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.anuncio = anuncio
            avaliacao.avaliador = request.user
            avaliacao.save()
            messages.success(request, 'Avaliação registrada com sucesso!')
            return redirect('servicos_produtos:detalhe_anuncio', pk=anuncio.pk)
    else:
        form = AvaliacaoForm()
    return render(request, 'servicos_produtos/avaliar_anuncio.html', {'form': form})

@login_required
def desativar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, criador=request.user)
    anuncio.status = 'inativo'
    anuncio.save()
    messages.success(request, 'Anúncio desativado com sucesso!')
    return redirect('servicos_produtos:detalhe_anuncio', pk=pk)

@login_required
def reativar_anuncio(request, pk):
    anuncio = get_object_or_404(Anuncio, pk=pk, criador=request.user)
    anuncio.status = 'ativo'
    anuncio.save()
    messages.success(request, 'Anúncio reativado com sucesso!')
    return redirect('servicos_produtos:detalhe_anuncio', pk=pk)
