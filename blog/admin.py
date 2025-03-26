from django.contrib import admin
from .models import Categoria, Post, Comentario

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug', 'data_criacao')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome', 'descricao')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'status', 'destaque', 'data_criacao')
    list_filter = ('status', 'categoria', 'destaque')
    prepopulated_fields = {'slug': ('titulo',)}
    search_fields = ('titulo', 'conteudo')
    date_hierarchy = 'data_criacao'
    ordering = ('-data_criacao',)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'post', 'aprovado', 'data_criacao')
    list_filter = ('aprovado', 'data_criacao')
    search_fields = ('autor__username', 'conteudo')
    date_hierarchy = 'data_criacao'
    ordering = ('-data_criacao',)
