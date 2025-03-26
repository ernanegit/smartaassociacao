from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('aberto', 'Aberto'),
        ('em_andamento', 'Em Andamento'),
        ('resolvido', 'Resolvido'),
        ('fechado', 'Fechado'),
    ]

    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='aberto')
    prioridade = models.CharField(max_length=20, choices=PRIORIDADE_CHOICES, default='media')
    autor = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tickets_criados')
    atualizado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='tickets_atualizados', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ['-data_criacao']
        verbose_name = 'Ticket'
        verbose_name_plural = 'Tickets'

    def __str__(self):
        return f"{self.titulo} - {self.autor.username}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.titulo}-{self.autor.id}")
        super().save(*args, **kwargs)

class ComentarioTicket(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao']
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'

    def __str__(self):
        return f"Comentário de {self.autor.username} em {self.ticket.titulo}"
