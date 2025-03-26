from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Categorias"

class Anuncio(models.Model):
    TIPO_CHOICES = [
        ('servico', 'Serviço'),
        ('produto', 'Produto'),
    ]

    CATEGORIA_CHOICES = [
        ('construcao', 'Construção'),
        ('limpeza', 'Limpeza'),
        ('jardinagem', 'Jardinagem'),
        ('outros', 'Outros'),
    ]

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
    ]

    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    preco = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    imagem = models.ImageField(upload_to='anuncios/', null=True, blank=True)
    contato = models.TextField()
    local = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ativo')
    criador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='anuncios')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

class Avaliacao(models.Model):
    anuncio = models.ForeignKey(Anuncio, on_delete=models.CASCADE, related_name='avaliacoes')
    avaliador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nota = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comentario = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-data_criacao']
        unique_together = ['anuncio', 'avaliador']

    def __str__(self):
        return f'Avaliação de {self.avaliador.get_full_name()} para {self.anuncio}'
