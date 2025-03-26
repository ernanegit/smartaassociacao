from django.contrib import admin
from .models import Ata

@admin.register(Ata)
class AtaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'categoria', 'data_reuniao', 'destaque', 'downloads')
    list_filter = ('categoria', 'destaque', 'data_reuniao')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_reuniao'
    ordering = ('-data_reuniao',)
