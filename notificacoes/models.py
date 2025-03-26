from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

User = get_user_model()

class TipoNotificacao(models.TextChoices):
    TICKET_COMENTARIO = 'ticket_comentario', 'Novo comentário em ticket'
    TICKET_STATUS = 'ticket_status', 'Status do ticket atualizado'
    BLOG_POST = 'blog_post', 'Novo post no blog'
    BLOG_COMENTARIO = 'blog_comentario', 'Novo comentário no blog'
    ATA_NOVA = 'ata_nova', 'Nova ata publicada'
    SERVICO_NOVO = 'servico_novo', 'Novo serviço cadastrado'

class Notificacao(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notificacoes')
    tipo = models.CharField(max_length=50, choices=TipoNotificacao.choices)
    titulo = models.CharField(max_length=200)
    mensagem = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    lida = models.BooleanField(default=False)
    data_criacao = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Notificação'
        verbose_name_plural = 'Notificações'

    def __str__(self):
        return f"{self.titulo} - {self.usuario.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.tipo}-{self.titulo}-{self.usuario.id}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        if self.link:
            return self.link
        return reverse('notificacoes:detalhe', kwargs={'slug': self.slug})

    def marcar_como_lida(self):
        self.lida = True
        self.save()

    @classmethod
    def criar_notificacao(cls, usuario, tipo, titulo, mensagem, link=''):
        return cls.objects.create(
            usuario=usuario,
            tipo=tipo,
            titulo=titulo,
            mensagem=mensagem,
            link=link
        )
