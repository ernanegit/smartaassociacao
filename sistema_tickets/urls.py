from django.urls import path
from . import views

app_name = 'sistema_tickets'

urlpatterns = [
    path('', views.lista_tickets, name='lista_tickets'),
    path('novo/', views.criar_ticket, name='criar_ticket'),
    path('<int:pk>/', views.detalhe_ticket, name='detalhe_ticket'),
    path('<int:pk>/editar/', views.editar_ticket, name='editar_ticket'),
    path('<int:pk>/fechar/', views.fechar_ticket, name='fechar_ticket'),
    path('<int:pk>/comentar/', views.adicionar_comentario, name='adicionar_comentario'),
] 