from .models import Notificacao, TipoNotificacao

def notificar_ticket_comentario(ticket, comentario):
    """Notifica o autor do ticket sobre um novo comentário."""
    if ticket.autor != comentario.autor:
        Notificacao.criar_notificacao(
            usuario=ticket.autor,
            tipo=TipoNotificacao.TICKET_COMENTARIO,
            titulo=f'Novo comentário no ticket #{ticket.id}',
            mensagem=f'{comentario.autor.get_full_name()} comentou no seu ticket "{ticket.titulo}": {comentario.conteudo}',
            link=f'/tickets/{ticket.id}/'
        )

def notificar_ticket_status(ticket, status_anterior, status_novo):
    """Notifica o autor do ticket sobre uma mudança de status."""
    if ticket.autor != ticket.atualizado_por:
        Notificacao.criar_notificacao(
            usuario=ticket.autor,
            tipo=TipoNotificacao.TICKET_STATUS,
            titulo=f'Status do ticket #{ticket.id} atualizado',
            mensagem=f'O status do seu ticket "{ticket.titulo}" foi alterado de {status_anterior} para {status_novo} por {ticket.atualizado_por.get_full_name()}.',
            link=f'/tickets/{ticket.id}/'
        )

def notificar_blog_comentario(post, comentario):
    """Notifica o autor do post sobre um novo comentário."""
    if post.autor != comentario.autor:
        Notificacao.criar_notificacao(
            usuario=post.autor,
            tipo=TipoNotificacao.BLOG_COMENTARIO,
            titulo=f'Novo comentário no post "{post.titulo}"',
            mensagem=f'{comentario.autor.get_full_name()} comentou no seu post: {comentario.conteudo}',
            link=f'/blog/{post.slug}/'
        )

def notificar_ata_nova(ata):
    """Notifica todos os usuários sobre uma nova ata."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    for usuario in User.objects.filter(is_active=True):
        Notificacao.criar_notificacao(
            usuario=usuario,
            tipo=TipoNotificacao.ATA_NOVA,
            titulo=f'Nova ata publicada: {ata.titulo}',
            mensagem=f'Uma nova ata foi publicada: {ata.descricao}',
            link=f'/atas/{ata.slug}/'
        )

def notificar_servico_novo(servico):
    """Notifica todos os usuários sobre um novo serviço."""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    for usuario in User.objects.filter(is_active=True):
        Notificacao.criar_notificacao(
            usuario=usuario,
            tipo=TipoNotificacao.SERVICO_NOVO,
            titulo=f'Novo serviço cadastrado: {servico.titulo}',
            mensagem=f'Um novo serviço foi cadastrado: {servico.descricao}',
            link=f'/servicos/{servico.slug}/'
        ) 