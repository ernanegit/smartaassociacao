from django.urls import path
from . import views

app_name = 'notificacoes'

urlpatterns = [
    path('', views.lista_notificacoes, name='lista'),
    path('<slug:slug>/', views.detalhe_notificacao, name='detalhe'),
    path('<slug:slug>/marcar-lida/', views.marcar_como_lida, name='marcar_lida'),
    path('marcar-todas-lidas/', views.marcar_todas_como_lidas, name='marcar_todas_lidas'),
    path('contador/', views.obter_contador_notificacoes, name='contador'),
] 