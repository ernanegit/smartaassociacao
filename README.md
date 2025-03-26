# Sistema de Gestão de Associação de Moradores

Este é um sistema web desenvolvido em Django para gerenciar uma associação de moradores, oferecendo funcionalidades para gestão de tickets, serviços, blog e atas de reuniões.

## Funcionalidades

### Sistema de Tickets
- Criação e gerenciamento de tickets
- Categorização de tickets
- Sistema de prioridades
- Acompanhamento de status
- Comentários em tickets

### Serviços e Produtos
- Cadastro de serviços e produtos
- Categorização
- Sistema de busca
- Perfil de prestadores de serviço

### Blog
- Publicação de posts
- Categorização de conteúdo
- Sistema de comentários
- Destaques para posts importantes
- Upload de imagens

### Atas de Reuniões
- Registro de atas
- Categorização
- Upload de arquivos
- Controle de downloads
- Sistema de destaques

## Requisitos

- Python 3.8+
- Django 4.2+
- Pillow (para manipulação de imagens)
- django-cleanup (para limpeza automática de arquivos)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/associacao.git
cd associacao
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Execute as migrações:
```bash
python manage.py migrate
```

6. Crie um superusuário:
```bash
python manage.py createsuperuser
```

7. Inicie o servidor de desenvolvimento:
```bash
python manage.py runserver
```

## Estrutura do Projeto

```
associacao/
├── associacao/          # Configurações do projeto
├── core/               # Aplicação principal
├── sistema_tickets/    # Gestão de tickets
├── servicos_produtos/  # Gestão de serviços
├── blog/              # Sistema de blog
├── atas/              # Gestão de atas
├── templates/         # Templates HTML
├── static/           # Arquivos estáticos
└── media/            # Arquivos de mídia
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## Contato

Seu Nome - [@seu_twitter](https://twitter.com/seu_twitter) - email@exemplo.com

Link do Projeto: [https://github.com/seu-usuario/associacao](https://github.com/seu-usuario/associacao) 