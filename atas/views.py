# atas/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import FileResponse
from .models import Ata
from .forms import AtaForm

def lista_atas(request):
    atas = Ata.objects.all().order_by('-data_reuniao')
    
    # Filtro por categoria
    categoria = request.GET.get('categoria')
    if categoria:
        atas = atas.filter(categoria=categoria)
    
    # Filtro por busca
    busca = request.GET.get('busca')
    if busca:
        atas = atas.filter(
            Q(titulo__icontains=busca) |
            Q(descricao__icontains=busca)
        )
    
    # Ordenação
    ordenacao = request.GET.get('ordenacao', '-data_reuniao')
    atas = atas.order_by(ordenacao)
    
    # Paginação
    paginator = Paginator(atas, 12)  # 12 atas por página
    page = request.GET.get('page')
    atas = paginator.get_page(page)
    
    context = {
        'atas': atas,
        'categoria': categoria,
        'busca': busca,
        'ordenacao': ordenacao,
    }
    return render(request, 'atas/lista_atas.html', context)

def detalhe_ata(request, pk):
    ata = get_object_or_404(Ata, pk=pk)
    
    # Incrementa contador de downloads se houver download
    if request.GET.get('download'):
        ata.downloads += 1
        ata.save()
        return FileResponse(ata.arquivo, as_attachment=True)
    
    context = {
        'ata': ata,
    }
    return render(request, 'atas/detalhe_ata.html', context)

@user_passes_test(lambda u: u.is_staff)
def criar_ata(request):
    if request.method == 'POST':
        form = AtaForm(request.POST, request.FILES)
        if form.is_valid():
            ata = form.save(commit=False)
            ata.autor = request.user
            ata.save()
            messages.success(request, 'Ata criada com sucesso!')
            return redirect('atas:detalhe_ata', pk=ata.pk)
    else:
        form = AtaForm()
    
    context = {
        'form': form,
    }
    return render(request, 'atas/form_ata.html', context)

@user_passes_test(lambda u: u.is_staff)
def editar_ata(request, pk):
    ata = get_object_or_404(Ata, pk=pk)
    
    if request.method == 'POST':
        form = AtaForm(request.POST, request.FILES, instance=ata)
        if form.is_valid():
            ata = form.save()
            messages.success(request, 'Ata atualizada com sucesso!')
            return redirect('atas:detalhe_ata', pk=ata.pk)
    else:
        form = AtaForm(instance=ata)
    
    context = {
        'form': form,
        'ata': ata,
    }
    return render(request, 'atas/form_ata.html', context)