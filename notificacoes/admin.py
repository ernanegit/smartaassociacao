from django.contrib import admin
from .models import Notificacao

@admin.register(Notificacao)
class NotificacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'usuario', 'tipo', 'lida', 'data_criacao')
    list_filter = ('tipo', 'lida', 'data_criacao')
    search_fields = ('titulo', 'mensagem', 'usuario__username', 'usuario__first_name', 'usuario__last_name')
    readonly_fields = ('data_criacao', 'slug')
    ordering = ('-data_criacao',)
