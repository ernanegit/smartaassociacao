# populate_test_data.py
import os
import sys
import django

# Configuração do ambiente Django
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'associacao.settings')

# Inicializar Django
django.setup()

# Agora podemos importar os modelos
import random
import uuid
from datetime import datetime, timedelta
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

# Importando modelos
from cadastro_usuarios.models import PerfilMorador
from sistema_tickets.models import Categoria as CategoriaTicket, Ticket, ComentarioTicket
from servicos_produtos.models import Anuncio, Avaliacao
from blog.models import Categoria as CategoriaBlog, Post, Comentario
from atas.models import Ata

def gerar_cpf_unico():
    """Gera um CPF único para uso no banco de dados"""
    cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
    
    # Verifica se já existe no banco de dados
    while PerfilMorador.objects.filter(cpf=cpf).exists():
        cpf = f"{random.randint(100, 999)}.{random.randint(100, 999)}.{random.randint(100, 999)}-{random.randint(10, 99)}"
        
    return cpf

def criar_usuarios(quantidade=10):
    """Criar usuários de teste"""
    print("Criando usuários...")
    
    # Admin principal
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@associacao.com',
            'first_name': 'Administrador',
            'last_name': 'Sistema',
            'is_staff': True,
            'is_superuser': True
        }
    )
    
    if created:
        admin.set_password('admin123')
        admin.save()
        print(f"Usuário admin criado. Login: admin / Senha: admin123")
    
    # Outros usuários
    nomes = ['Maria', 'João', 'Ana', 'Pedro', 'Carla', 'Lucas', 'Fernanda', 'Rafael', 'Julia', 'Marcos', 
             'Tânia', 'Carlos', 'Camila', 'Paulo', 'Daniela']
    sobrenomes = ['Silva', 'Santos', 'Oliveira', 'Souza', 'Lima', 'Pereira', 'Costa', 'Rodrigues', 'Almeida', 
                 'Ferreira', 'Martins']
    
    usuarios_criados = []
    
    for i in range(quantidade):
        nome = random.choice(nomes)
        sobrenome = random.choice(sobrenomes)
        username = f"{nome.lower()}.{sobrenome.lower()}{random.randint(1, 99)}"
        
        # Tornar username único adicionando um ID
        while User.objects.filter(username=username).exists():
            username = f"{nome.lower()}.{sobrenome.lower()}{random.randint(1, 999)}"
            
        email = f"{username}@email.com"
        
        try:
            usuario = User.objects.create(
                username=username,
                email=email,
                first_name=nome,
                last_name=sobrenome,
                is_staff=random.random() < 0.2  # 20% de chance de ser staff
            )
            
            usuario.set_password('senha123')
            usuario.save()
            usuarios_criados.append(usuario)
            
            # Criar perfil do morador
            perfil = PerfilMorador(usuario=usuario)
            perfil.cpf = gerar_cpf_unico()
            perfil.telefone = f"({random.randint(10, 99)}) 9{random.randint(8000, 9999)}-{random.randint(1000, 9999)}"
            perfil.endereco = f"Rua das Flores, {random.randint(1, 500)}"
            perfil.numero_casa = str(random.randint(1, 999))
            perfil.data_nascimento = datetime.now() - timedelta(days=random.randint(7300, 25550))  # 20-70 anos
            perfil.save()
            
            print(f"Usuário {username} criado com sucesso!")
        except Exception as e:
            print(f"Erro ao criar usuário {username}: {e}")
    
    print(f"{len(usuarios_criados)} usuários criados com senha 'senha123'")
    return usuarios_criados + [admin]

def criar_categorias_tickets():
    """Criar categorias de tickets"""
    print("Criando categorias de tickets...")
    
    categorias = [
        {'nome': 'Manutenção', 'slug': 'manutencao', 'descricao': 'Problemas de manutenção nas áreas comuns'},
        {'nome': 'Segurança', 'slug': 'seguranca', 'descricao': 'Questões relacionadas à segurança do condomínio'},
        {'nome': 'Barulho', 'slug': 'barulho', 'descricao': 'Reclamações sobre barulho excessivo'},
        {'nome': 'Limpeza', 'slug': 'limpeza', 'descricao': 'Problemas com limpeza das áreas comuns'},
        {'nome': 'Sugestões', 'slug': 'sugestoes', 'descricao': 'Sugestões para melhorias no condomínio'},
    ]
    
    categorias_criadas = []
    
    for categoria_data in categorias:
        try:
            categoria, created = CategoriaTicket.objects.get_or_create(
                slug=categoria_data['slug'],
                defaults={
                    'nome': categoria_data['nome'],
                    'descricao': categoria_data['descricao']
                }
            )
            categorias_criadas.append(categoria)
        except Exception as e:
            print(f"Erro ao criar categoria {categoria_data['nome']}: {e}")
    
    print(f"{len(categorias_criadas)} categorias de tickets criadas ou atualizadas")
    return categorias_criadas

def criar_tickets(usuarios, categorias, quantidade=30):
    """Criar tickets de teste"""
    print("Criando tickets...")
    
    if not categorias:
        print("Não há categorias disponíveis para criar tickets")
        return []
    
    titulos = [
        "Vazamento no corredor do bloco 3",
        "Lâmpada queimada na garagem",
        "Barulho excessivo no apartamento 102",
        "Infiltração na parede do salão de festas",
        "Porta do elevador com problema",
        "Interfone não está funcionando",
        "Sujeira na piscina",
        "Problema com a bomba d'água",
        "Sugestão para nova área de lazer",
        "Reclamação sobre lixo mal acondicionado"
    ]
    
    status_opcoes = ['aberto', 'em_andamento', 'resolvido', 'fechado']
    prioridade_opcoes = ['baixa', 'media', 'alta', 'urgente']
    
    tickets_criados = []
    
    for i in range(quantidade):
        try:
            titulo = random.choice(titulos) + f" #{i+1}"
            descricao = f"Descrição do problema: {titulo}. " + \
                        f"Este é um ticket de teste criado automaticamente. " + \
                        f"Por favor, verificar o problema o mais rápido possível."
            
            autor = random.choice(usuarios)
            categoria = random.choice(categorias)
            
            # Datas aleatórias nos últimos 60 dias
            dias_atras = random.randint(0, 60)
            data_criacao = datetime.now() - timedelta(days=dias_atras)
            
            ticket = Ticket(
                titulo=titulo,
                descricao=descricao,
                categoria=categoria,
                status=random.choice(status_opcoes),
                prioridade=random.choice(prioridade_opcoes),
                autor=autor,
                atualizado_por=random.choice(usuarios),
                data_criacao=data_criacao
            )
            
            # Criar slug manualmente - garantimos que seja único
            base_slug = slugify(f"{ticket.titulo}-{ticket.autor.id}")
            slug = base_slug
            counter = 1
            
            while Ticket.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
                
            ticket.slug = slug
            ticket.save()
            tickets_criados.append(ticket)
            
            # Adicionar alguns comentários
            num_comentarios = random.randint(0, 3)
            for j in range(num_comentarios):
                comentario = ComentarioTicket(
                    ticket=ticket,
                    autor=random.choice(usuarios),
                    conteudo=f"Este é um comentário de teste #{j+1} para o ticket '{ticket.titulo}'.",
                    data_criacao=ticket.data_criacao + timedelta(days=random.randint(1, 5))
                )
                comentario.save()
        except Exception as e:
            print(f"Erro ao criar ticket {i+1}: {e}")
    
    print(f"{len(tickets_criados)} tickets criados")
    return tickets_criados

def criar_anuncios(usuarios, quantidade=20):
    """Criar anúncios de serviços e produtos"""
    print("Criando anúncios...")
    
    titulos_servicos = [
        "Serviço de encanador profissional",
        "Eletricista residencial",
        "Aulas particulares de matemática",
        "Conserto de computadores e notebooks",
        "Babá experiente disponível",
        "Serviço de limpeza residencial",
        "Pintor profissional",
        "Passeador de cães",
        "Personal trainer",
        "Professora de inglês"
    ]
    
    titulos_produtos = [
        "Geladeira seminova",
        "Sofá em ótimo estado",
        "Mesa de jantar com 6 cadeiras",
        "Bicicleta aro 26",
        "Livros de engenharia",
        "Televisão 42 polegadas",
        "Videogame usado",
        "Celular com poucos meses de uso",
        "Cama box casal",
        "Armário de cozinha completo"
    ]
    
    tipos = ['servico', 'produto']
    categorias = ['construcao', 'limpeza', 'jardinagem', 'outros']
    
    anuncios_criados = []
    
    for i in range(quantidade):
        try:
            tipo = random.choice(tipos)
            
            if tipo == 'servico':
                titulo = random.choice(titulos_servicos)
                descricao = f"Ofereço serviço de {titulo.lower()}. Tenho experiência e boas referências. Entre em contato para mais informações."
                preco = random.randint(50, 200)
            else:
                titulo = random.choice(titulos_produtos)
                descricao = f"Vendo {titulo.lower()} em ótimo estado. Pouco tempo de uso. Aceito propostas."
                preco = random.randint(100, 2000)
            
            # Datas aleatórias nos últimos 90 dias
            dias_atras = random.randint(0, 90)
            data_criacao = datetime.now() - timedelta(days=dias_atras)
            
            anuncio = Anuncio(
                titulo=f"{titulo} #{i+1}",
                descricao=descricao,
                tipo=tipo,
                categoria=random.choice(categorias),
                preco=preco,
                contato=f"Contato: {random.choice(['Telefone', 'WhatsApp', 'Email'])}: " + 
                       f"{random.choice(usuarios).email if random.random() > 0.5 else '(99) 99999-9999'}",
                local=f"Bloco {random.randint(1, 10)}, Apartamento {random.randint(101, 999)}",
                status='ativo',
                criador=random.choice(usuarios),
                data_criacao=data_criacao
            )
            anuncio.save()
            anuncios_criados.append(anuncio)
            
            # Adicionar algumas avaliações
            num_avaliacoes = random.randint(0, 3)
            usuarios_avaliadores = random.sample(list(usuarios), min(num_avaliacoes, len(usuarios)))
            
            for usuario in usuarios_avaliadores:
                if usuario != anuncio.criador:  # Não permitir auto-avaliação
                    avaliacao = Avaliacao(
                        anuncio=anuncio,
                        avaliador=usuario,
                        nota=random.randint(3, 5),  # Tendência para notas mais altas
                        comentario=f"Ótimo {tipo}! Recomendo a todos.",
                        data_criacao=anuncio.data_criacao + timedelta(days=random.randint(1, 30))
                    )
                    avaliacao.save()
        except Exception as e:
            print(f"Erro ao criar anúncio {i+1}: {e}")
    
    print(f"{len(anuncios_criados)} anúncios criados")
    return anuncios_criados

def criar_categorias_blog():
    """Criar categorias de blog"""
    print("Criando categorias de blog...")
    
    categorias = [
        {'nome': 'Notícias', 'slug': 'noticias', 'descricao': 'Notícias sobre a associação e o bairro'},
        {'nome': 'Eventos', 'slug': 'eventos', 'descricao': 'Eventos promovidos pela associação'},
        {'nome': 'Dicas', 'slug': 'dicas', 'descricao': 'Dicas úteis para os moradores'},
        {'nome': 'Entrevistas', 'slug': 'entrevistas', 'descricao': 'Entrevistas com moradores e personalidades'},
        {'nome': 'Legislação', 'slug': 'legislacao', 'descricao': 'Informações sobre leis e regulamentos'},
    ]
    
    categorias_criadas = []
    
    for categoria_data in categorias:
        try:
            categoria, created = CategoriaBlog.objects.get_or_create(
                slug=categoria_data['slug'],
                defaults={
                    'nome': categoria_data['nome'],
                    'descricao': categoria_data['descricao']
                }
            )
            categorias_criadas.append(categoria)
        except Exception as e:
            print(f"Erro ao criar categoria de blog {categoria_data['nome']}: {e}")
    
    print(f"{len(categorias_criadas)} categorias de blog criadas ou atualizadas")
    return categorias_criadas

def criar_posts(usuarios, categorias, quantidade=15):
    """Criar posts de blog"""
    print("Criando posts de blog...")
    
    if not categorias:
        print("Não há categorias disponíveis para criar posts")
        return []
    
    titulos = [
        "Assembleia geral aprova novo regulamento",
        "Festa junina será realizada no próximo mês",
        "Dicas de economia de água para moradores",
        "Entrevista com o síndico sobre melhorias",
        "Nova área de lazer será inaugurada em breve",
        "Campanha de reciclagem bate recorde",
        "Conheça os novos membros da diretoria",
        "Obras de manutenção começam na próxima semana",
        "Resultados da pesquisa de satisfação",
        "Novas regras para uso da área de lazer"
    ]
    
    status_opcoes = ['rascunho', 'publicado', 'arquivado']
    
    posts_criados = []
    
    for i in range(quantidade):
        try:
            titulo = random.choice(titulos) + f" #{i+1}"
            
            conteudo_html = f"""
            <h2>Introdução</h2>
            <p>Este é um post de teste sobre "{titulo}".</p>
            <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies ultricies, 
            nunc nisl aliquam nunc, vitae aliquam nisl nisl vitae nisl.</p>
            
            <h2>Desenvolvimento</h2>
            <p>Sed et consequat nisl, eget euismod nisl. Nullam euismod, nisl eget ultricies ultricies,
            nunc nisl aliquam nunc, vitae aliquam nisl nisl vitae nisl.</p>
            <ul>
                <li>Item 1</li>
                <li>Item 2</li>
                <li>Item 3</li>
            </ul>
            
            <h2>Conclusão</h2>
            <p>Nullam euismod, nisl eget ultricies ultricies, nunc nisl aliquam nunc, vitae aliquam nisl nisl vitae nisl.</p>
            """
            
            # Datas aleatórias nos últimos 180 dias
            dias_atras = random.randint(0, 180)
            data_criacao = datetime.now() - timedelta(days=dias_atras)
            
            autor = random.choice(usuarios)
            categoria = random.choice(categorias)
            
            # Criar post com slug único
            base_slug = slugify(titulo)
            slug = base_slug
            counter = 1
            
            while Post.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            post = Post(
                titulo=titulo,
                slug=slug,
                autor=autor,
                categoria=categoria,
                conteudo=conteudo_html,
                data_criacao=data_criacao,
                status=random.choices(status_opcoes, weights=[0.1, 0.8, 0.1])[0],  # 80% chance de estar publicado
                destaque=random.random() < 0.2,  # 20% chance de ser destaque
                visualizacoes=random.randint(0, 100)
            )
            
            post.save()
            posts_criados.append(post)
            
            # Adicionar alguns comentários
            num_comentarios = random.randint(0, 3)
            for j in range(num_comentarios):
                comentario = Comentario(
                    post=post,
                    autor=random.choice(usuarios),
                    conteudo=f"Este é um comentário de teste #{j+1} para o post '{post.titulo}'.",
                    aprovado=True,
                    data_criacao=post.data_criacao + timedelta(days=random.randint(1, 10))
                )
                comentario.save()
        except Exception as e:
            print(f"Erro ao criar post {i+1}: {e}")
    
    print(f"{len(posts_criados)} posts criados")
    return posts_criados

def criar_atas(usuarios, quantidade=10):
    """Criar atas de reuniões"""
    print("Criando atas de reuniões...")
    
    admin_users = [u for u in usuarios if u.is_staff]
    if not admin_users:
        print("Não há usuários admin disponíveis para criar atas")
        return []
    
    titulos = [
        "Ata da Assembleia Geral Ordinária",
        "Ata da Reunião do Conselho Deliberativo",
        "Ata da Reunião de Diretoria",
        "Ata da Assembleia Geral Extraordinária",
        "Ata da Reunião de Prestação de Contas",
        "Ata da Reunião sobre Obras e Manutenção",
        "Ata da Reunião sobre Segurança",
        "Ata da Eleição da Nova Diretoria",
        "Ata da Reunião sobre Eventos",
        "Ata da Reunião de Planejamento Anual"
    ]
    
    categorias = ['assembleia', 'conselho', 'diretoria', 'outros']
    
    atas_criadas = []
    
    # Criar um arquivo de texto simples para simular o PDF da ata
    content = "Este é um arquivo de teste para simular uma ata de reunião."
    
    for i in range(quantidade):
        try:
            titulo = random.choice(titulos) + f" #{i+1}"
            
            # Datas aleatórias nos últimos 365 dias
            dias_atras = random.randint(0, 365)
            data_reuniao = datetime.now().date() - timedelta(days=dias_atras)
            
            autor = random.choice(admin_users)
            categoria = random.choice(categorias)
            
            # Criar um arquivo para a ata - garantir nome de arquivo único
            filename = f'ata_{i+1}_{uuid.uuid4().hex[:8]}.txt'
            
            # Criar um arquivo para a ata
            ata = Ata(
                titulo=titulo,
                descricao=f"Esta é a ata da reunião '{titulo}' realizada em {data_reuniao}. " +
                        f"Foram discutidos assuntos importantes relacionados à associação de moradores.",
                data_reuniao=data_reuniao,
                autor=autor,
                categoria=categoria,
                destaque=random.random() < 0.3,  # 30% chance de ser destaque
                downloads=random.randint(0, 50)
            )
            
            # Criar um arquivo de texto simples e associá-lo ao campo de arquivo
            file_content = ContentFile(content.encode('utf-8'))
            ata.arquivo.save(filename, file_content)
            
            ata.save()
            atas_criadas.append(ata)
        except Exception as e:
            print(f"Erro ao criar ata {i+1}: {e}")
    
    print(f"{len(atas_criadas)} atas criadas")
    return atas_criadas

if __name__ == "__main__":
    print("Iniciando população de dados de teste...")
    
    try:
        # Criar usuários primeiro
        usuarios = criar_usuarios(quantidade=15)
        
        # Criar categorias de tickets
        categorias_tickets = criar_categorias_tickets()
        
        # Criar tickets
        tickets = criar_tickets(usuarios, categorias_tickets, quantidade=30)
        
        # Criar anúncios
        anuncios = criar_anuncios(usuarios, quantidade=20)
        
        # Criar categorias de blog
        categorias_blog = criar_categorias_blog()
        
        # Criar posts
        posts = criar_posts(usuarios, categorias_blog, quantidade=15)
        
        # Criar atas
        atas = criar_atas(usuarios, quantidade=10)
        
        print("Dados de teste criados com sucesso!")
        print("\nDetalhes:")
        print(f"- {len(usuarios)} usuários")
        print(f"- {len(categorias_tickets)} categorias de tickets")
        print(f"- {len(tickets)} tickets")
        print(f"- {len(anuncios)} anúncios")
        print(f"- {len(categorias_blog)} categorias de blog")
        print(f"- {len(posts)} posts")
        print(f"- {len(atas)} atas")
        
        print("\nAcesso admin:")
        print("Username: admin")
        print("Senha: admin123")
        print("\nAcesso usuários comuns:")
        print("Senha padrão para todos os usuários: senha123")
    
    except Exception as e:
        print(f"Erro durante a execução do script: {e}")