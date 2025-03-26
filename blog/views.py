from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import Post, Categoria, Comentario
from .forms import PostForm, ComentarioForm

def lista_posts(request):
    posts = Post.objects.filter(status='publicado')
    categorias = Categoria.objects.all()
    
    # Filtro por categoria
    categoria_slug = request.GET.get('categoria')
    if categoria_slug:
        posts = posts.filter(categoria__slug=categoria_slug)
    
    # Filtro por busca
    query = request.GET.get('q')
    if query:
        posts = posts.filter(titulo__icontains=query) | posts.filter(conteudo__icontains=query)
    
    # Ordenação
    ordenacao = request.GET.get('ordenacao', '-data_criacao')
    posts = posts.order_by(ordenacao)
    
    # Paginação
    paginator = Paginator(posts, 9)  # 9 posts por página
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'posts': posts,
        'categorias': categorias,
        'categoria_atual': categoria_slug,
        'query': query,
    }
    return render(request, 'blog/lista_posts.html', context)

def detalhe_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='publicado')
    comentarios = post.comentarios.filter(aprovado=True)
    
    # Incrementa visualizações
    post.incrementar_visualizacoes()
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.post = post
            comentario.autor = request.user
            comentario.save()
            messages.success(request, 'Comentário enviado com sucesso! Aguardando aprovação.')
            return redirect('blog:detalhe_post', slug=slug)
    else:
        form = ComentarioForm()
    
    context = {
        'post': post,
        'comentarios': comentarios,
        'form': form,
    }
    return render(request, 'blog/detalhe_post.html', context)

@login_required
def criar_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor = request.user
            post.slug = slugify(post.titulo)
            post.save()
            messages.success(request, 'Post criado com sucesso!')
            return redirect('blog:detalhe_post', slug=post.slug)
    else:
        form = PostForm()
    
    return render(request, 'blog/criar_post.html', {'form': form})

@login_required
def editar_post(request, slug):
    post = get_object_or_404(Post, slug=slug, autor=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'Post atualizado com sucesso!')
            return redirect('blog:detalhe_post', slug=post.slug)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'blog/editar_post.html', {'form': form, 'post': post})

def categoria(request, slug):
    categoria = get_object_or_404(Categoria, slug=slug)
    posts = Post.objects.filter(categoria=categoria, status='publicado')
    
    # Paginação
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    context = {
        'categoria': categoria,
        'posts': posts,
    }
    return render(request, 'blog/categoria.html', context)
