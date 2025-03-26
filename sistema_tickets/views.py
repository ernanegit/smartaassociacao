from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ticket, ComentarioTicket
from .forms import TicketForm, ComentarioForm
from notificacoes.utils import notificar_ticket_comentario, notificar_ticket_status

@login_required
def lista_tickets(request):
    tickets = Ticket.objects.filter(autor=request.user).order_by('-data_criacao')
    return render(request, 'sistema_tickets/lista_tickets.html', {'tickets': tickets})

@login_required
def criar_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.autor = request.user
            ticket.save()
            messages.success(request, 'Ticket criado com sucesso!')
            return redirect('sistema_tickets:detalhe_ticket', pk=ticket.pk)
    else:
        form = TicketForm()
    return render(request, 'sistema_tickets/criar_ticket.html', {'form': form})

@login_required
def detalhe_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, autor=request.user)
    comentarios = ticket.comentarios.all().order_by('-data_criacao')
    
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()
            
            # Enviar notificação sobre o novo comentário
            notificar_ticket_comentario(ticket, comentario)
            
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('sistema_tickets:detalhe_ticket', pk=pk)
    else:
        form = ComentarioForm()
    
    return render(request, 'sistema_tickets/detalhe_ticket.html', {
        'ticket': ticket,
        'comentarios': comentarios,
        'form': form
    })

@login_required
def editar_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            status_anterior = ticket.status
            ticket = form.save(commit=False)
            ticket.atualizado_por = request.user
            ticket.save()
            
            # Enviar notificação sobre a mudança de status
            if status_anterior != ticket.status:
                notificar_ticket_status(ticket, status_anterior, ticket.status)
            
            messages.success(request, 'Ticket atualizado com sucesso!')
            return redirect('sistema_tickets:detalhe_ticket', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket)
    
    return render(request, 'sistema_tickets/editar_ticket.html', {'form': form, 'ticket': ticket})

@login_required
def fechar_ticket(request, pk):
    if not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para fechar tickets.')
        return redirect('sistema_tickets:detalhe_ticket', pk=pk)
    
    ticket = get_object_or_404(Ticket, pk=pk)
    ticket.status = 'fechado'
    ticket.atualizado_por = request.user
    ticket.save()
    
    # Enviar notificação sobre a mudança de status
    notificar_ticket_status(ticket, 'aberto', 'fechado')
    
    messages.success(request, 'Ticket fechado com sucesso!')
    return redirect('sistema_tickets:detalhe_ticket', pk=ticket.pk)

@login_required
def adicionar_comentario(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.ticket = ticket
            comentario.autor = request.user
            comentario.save()
            
            # Enviar notificação sobre o novo comentário
            notificar_ticket_comentario(ticket, comentario)
            
            messages.success(request, 'Comentário adicionado com sucesso!')
            return redirect('sistema_tickets:detalhe_ticket', pk=ticket.pk)
    else:
        form = ComentarioForm()
    return render(request, 'sistema_tickets/adicionar_comentario.html', {'form': form})
