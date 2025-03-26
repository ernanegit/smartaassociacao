from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse('blog:categoria', kwargs={'slug': self.slug})

class Post(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    conteudo = RichTextField()
    imagem = models.ImageField(upload_to='blog/', null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
        ('arquivado', 'Arquivado')
    ], default='rascunho')
    destaque = models.BooleanField(default=False)
    visualizacoes = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse('blog:detalhe_post', kwargs={'slug': self.slug})

    def incrementar_visualizacoes(self):
        self.visualizacoes += 1
        self.save()

class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    conteudo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    aprovado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data_criacao']

    def __str__(self):
        return f'Comentário de {self.autor} em {self.post}'
