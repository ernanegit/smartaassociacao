from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class PerfilMorador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15)
    endereco = models.CharField(max_length=200)
    numero_casa = models.CharField(max_length=10)
    data_nascimento = models.DateField(null=True, blank=True)
    foto_perfil = models.ImageField(upload_to='perfil/', null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.cpf}"

@receiver(post_save, sender=User)
def criar_perfil_morador(sender, instance, created, **kwargs):
    if created:
        PerfilMorador.objects.create(usuario=instance)
