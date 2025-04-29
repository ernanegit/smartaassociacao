# atas/models.py
from django.db import models
from django.conf import settings
from django.urls import reverse

class Ata(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    arquivo = models.FileField(upload_to='atas/')
    data_reuniao = models.DateField()
    data_publicacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=50, choices=[
        ('assembleia', 'Assembleia Geral'),
        ('conselho', 'Conselho Deliberativo'),
        ('diretoria', 'Diretoria'),
        ('outros', 'Outros')
    ])
    destaque = models.BooleanField(default=False)
    downloads = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Ata'
        verbose_name_plural = 'Atas'
        ordering = ['-data_reuniao']

    def __str__(self):
        return f'{self.titulo} - {self.data_reuniao}'

    def get_absolute_url(self):
        return reverse('atas:detalhe_ata', kwargs={'pk': self.pk})

    def incrementar_downloads(self):
        self.downloads += 1
        self.save()