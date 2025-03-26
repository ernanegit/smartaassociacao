from django.urls import path
from . import views

app_name = 'servicos_produtos'

urlpatterns = [
    path('', views.lista_anuncios, name='lista_anuncios'),
    path('novo/', views.criar_anuncio, name='criar_anuncio'),
    path('<int:pk>/', views.detalhe_anuncio, name='detalhe_anuncio'),
    path('<int:pk>/editar/', views.editar_anuncio, name='editar_anuncio'),
    path('<int:pk>/excluir/', views.excluir_anuncio, name='excluir_anuncio'),
    path('<int:pk>/avaliar/', views.avaliar_anuncio, name='avaliar_anuncio'),
    path('<int:pk>/desativar/', views.desativar_anuncio, name='desativar_anuncio'),
    path('<int:pk>/reativar/', views.reativar_anuncio, name='reativar_anuncio'),
] 