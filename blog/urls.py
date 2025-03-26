from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.lista_posts, name='lista_posts'),
    path('novo/', views.criar_post, name='criar_post'),
    path('<slug:slug>/', views.detalhe_post, name='detalhe_post'),
    path('<slug:slug>/editar/', views.editar_post, name='editar_post'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
] 