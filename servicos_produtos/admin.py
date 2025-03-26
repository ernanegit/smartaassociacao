from django.contrib import admin
from .models import Anuncio, Avaliacao

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'criador', 'tipo', 'categoria', 'preco', 'data_criacao')
    list_filter = ('tipo', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'criador__first_name', 'criador__last_name')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'imagem')
        }),
        ('Categorização', {
            'fields': ('tipo', 'categoria')
        }),
        ('Preço e Localização', {
            'fields': ('preco', 'local')
        }),
        ('Contato', {
            'fields': ('contato',)
        }),
        ('Informações Adicionais', {
            'fields': ('criador', 'data_criacao', 'data_atualizacao')
        }),
    )

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('anuncio', 'avaliador', 'nota', 'data_criacao')
    list_filter = ('nota', 'data_criacao')
    search_fields = ('comentario', 'avaliador__first_name', 'avaliador__last_name', 'anuncio__titulo')
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Avaliação', {
            'fields': ('anuncio', 'nota', 'comentario')
        }),
        ('Informações Adicionais', {
            'fields': ('avaliador', 'data_criacao')
        }),
    )
