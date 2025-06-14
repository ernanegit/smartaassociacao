# Generated by Django 5.1.7 on 2025-03-26 14:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilMorador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('telefone', models.CharField(max_length=15)),
                ('endereco', models.CharField(max_length=200)),
                ('numero_casa', models.CharField(max_length=10)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('foto_perfil', models.ImageField(blank=True, null=True, upload_to='perfil/')),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('ativo', models.BooleanField(default=True)),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
