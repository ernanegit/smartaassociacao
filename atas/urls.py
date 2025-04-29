from django.urls import path
from . import views

app_name = 'atas'

urlpatterns = [
    path('', views.lista_atas, name='lista_atas'),
    path('nova/', views.criar_ata, name='criar_ata'),
    path('<int:pk>/', views.detalhe_ata, name='detalhe_ata'),
    path('<int:pk>/editar/', views.editar_ata, name='editar_ata'),
]