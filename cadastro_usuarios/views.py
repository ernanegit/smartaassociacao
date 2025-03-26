from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegistroForm, PerfilForm

# Create your views here.

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'cadastro_usuarios/registro.html', {'form': form})

@login_required
def perfil(request):
    return render(request, 'cadastro_usuarios/perfil.html')

@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=request.user.perfilmorador)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('usuarios:perfil')
    else:
        form = PerfilForm(instance=request.user.perfilmorador)
    return render(request, 'cadastro_usuarios/editar_perfil.html', {'form': form})
