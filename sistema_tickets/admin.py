from django.contrib import admin
from .models import Categoria, Ticket, ComentarioTicket
from django.utils.html import format_html

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'slug')
    prepopulated_fields = {'slug': ('nome',)}
    search_fields = ('nome',)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'status', 'prioridade', 'data_criacao')
    list_filter = ('status', 'prioridade', 'categoria', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'autor__username', 'autor__first_name', 'autor__last_name')
    readonly_fields = ('data_criacao', 'data_atualizacao', 'slug')
    date_hierarchy = 'data_criacao'
    list_editable = ('status', 'prioridade')
    actions = ['marcar_como_resolvido', 'marcar_como_em_andamento', 'marcar_como_fechado']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'status', 'prioridade')
        }),
        ('Informações do Autor', {
            'fields': ('autor', 'categoria')
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )

    def colored_status(self, obj):
        colors = {
            'aberto': '#28a745',  # Verde
            'em_andamento': '#ffc107',  # Amarelo
            'resolvido': '#17a2b8',  # Azul claro
            'fechado': '#6c757d',  # Cinza
        }
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 4px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status Visual'
    colored_status.admin_order_field = 'status'

    def marcar_como_resolvido(self, request, queryset):
        queryset.update(status='resolvido')
    marcar_como_resolvido.short_description = "Marcar tickets selecionados como resolvidos"

    def marcar_como_em_andamento(self, request, queryset):
        queryset.update(status='em_andamento')
    marcar_como_em_andamento.short_description = "Marcar tickets selecionados como em andamento"

    def marcar_como_fechado(self, request, queryset):
        queryset.update(status='fechado')
    marcar_como_fechado.short_description = "Marcar tickets selecionados como fechados"

@admin.register(ComentarioTicket)
class ComentarioTicketAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'autor', 'data_criacao')
    list_filter = ('data_criacao', 'autor')
    search_fields = ('conteudo', 'autor__username', 'autor__first_name', 'autor__last_name', 'ticket__titulo')
    readonly_fields = ('data_criacao',)
