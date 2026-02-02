# Star Wars API

API REST desenvolvida em FastAPI que integra com a [SWAPI (Star Wars API)](https://swapi.dev/) para fornecer informações sobre o universo Star Wars, incluindo filmes, personagens, planetas, espécies, naves espaciais e veículos.

## 📋 Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Endpoints da API](#endpoints-da-api)
- [Autenticação](#autenticação)
- [Docker](#docker)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Contribuindo](#contribuindo)

## 🎯 Sobre o Projeto

Esta API foi desenvolvida como um projeto técnico que demonstra a integração com APIs externas, implementação de autenticação JWT, gerenciamento de banco de dados NoSQL (MongoDB), cache com Redis, e uma arquitetura RESTful moderna utilizando FastAPI.

## ✨ Funcionalidades

- **Consulta de Dados Star Wars**: Acesso a informações sobre filmes, personagens, planetas, espécies, naves espaciais e veículos
- **Expansão de Dados**: Opção de expandir dados relacionados (ex: obter informações completas de personagens ao invés de apenas URLs)
- **Paginação**: Suporte a paginação nos endpoints de listagem
- **Ordenação**: Possibilidade de ordenar resultados por diferentes campos
- **Autenticação JWT**: Sistema de autenticação seguro usando JSON Web Tokens
- **Favoritos**: Usuários podem salvar seus itens favoritos
- **Comentários**: Sistema de comentários para itens específicos
- **Cache Redis**: Cache inteligente para melhorar performance e reduzir chamadas à API externa
- **Documentação Interativa**: Documentação automática com Swagger UI

## 🛠 Tecnologias Utilizadas

- **FastAPI**: Framework web moderno e rápido para construção de APIs
- **Python 3.14**: Linguagem de programação
- **MongoDB**: Banco de dados NoSQL para armazenamento de usuários, favoritos e comentários
- **Redis**: Sistema de cache em memória
- **Pydantic**: Validação de dados e configurações
- **JWT**: Autenticação baseada em tokens
- **bcrypt**: Hash de senhas
- **httpx**: Cliente HTTP assíncrono para integração com SWAPI
- **Docker & Docker Compose**: Containerização e orquestração
- **Uvicorn**: Servidor ASGI de alta performance

## 📦 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- Python 3.14 ou superior
- Docker e Docker Compose (opcional, para uso com containers)
- MongoDB (se não estiver usando Docker)
- Redis (se não estiver usando Docker)

## 🚀 Instalação

### Instalação Local

1. Clone o repositório:
```bash
git clone <url-do-repositório>
cd starwars
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente (veja seção [Configuração](#configuração))

5. Execute a aplicação:
```bash
uvicorn main:app --reload
```

A API estará disponível em `http://localhost:8000`

### Instalação com Docker

1. Clone o repositório:
```bash
git clone <url-do-repositório>
cd starwars
```

2. Crie um arquivo `.env` com suas configurações (veja seção [Configuração](#configuração))

3. Execute com Docker Compose:
```bash
docker-compose up -d
```

A API estará disponível em `http://localhost:8080`

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
BASE_URL=https://swapi.dev/api/
SECRET_KEY=sua-chave-secreta-aqui
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
MONGO_URI=mongodb://usuario:senha@localhost:27017/starwars?authSource=admin
MONGO_DB=starwars
MONGO_USERNAME=admin
MONGO_PASSWORD=admin123
MONGO_HOST=localhost
MONGO_PORT=27017
REDIS_URL=redis://localhost:6379
```

**Nota**: Se `MONGO_URI` não for fornecido, a aplicação construirá automaticamente a URI usando as outras variáveis do MongoDB.

## 📖 Uso

### Documentação Interativa

Após iniciar a aplicação, acesse:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Exemplo de Requisição

```bash
# Obter todos os filmes
curl http://localhost:8000/films

# Obter um filme específico com dados expandidos
curl http://localhost:8000/films/1?species=true&people=true

# Registrar um novo usuário
curl -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "usuario", "password": "senha123"}'

# Fazer login
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario&password=senha123"
```

## 🔌 Endpoints da API

### Autenticação

- `POST /register` - Registrar novo usuário
- `POST /token` - Obter token de autenticação (OAuth2)
- `DELETE /user` - Deletar usuário (requer autenticação)

### Filmes

- `GET /films` - Listar todos os filmes
  - Query params: `species`, `people`, `starships`, `vehicles`, `planets` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /films/{film_id}` - Obter filme por ID
  - Query params: `species`, `people`, `starships`, `vehicles`, `planets` (boolean)

### Personagens

- `GET /people` - Listar todos os personagens
  - Query params: `films`, `species`, `starships`, `vehicles`, `homeworld` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /people/{people_id}` - Obter personagem por ID
  - Query params: `films`, `species`, `starships`, `vehicles`, `homeworld` (boolean)

### Planetas

- `GET /planets` - Listar todos os planetas
  - Query params: `residents`, `films` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /planets/{planet_id}` - Obter planeta por ID
  - Query params: `residents`, `films` (boolean)

### Espécies

- `GET /species` - Listar todas as espécies
  - Query params: `homeworld`, `films`, `people` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /species/{species_id}` - Obter espécie por ID
  - Query params: `homeworld`, `films`, `people` (boolean)

### Naves Espaciais

- `GET /starships` - Listar todas as naves espaciais
  - Query params: `films`, `pilots` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /starships/{starship_id}` - Obter nave espacial por ID
  - Query params: `films`, `pilots` (boolean)

### Veículos

- `GET /vehicles` - Listar todos os veículos
  - Query params: `films`, `pilots` (boolean), `page`, `n`, `order_by`, `order_direction`
- `GET /vehicles/{vehicle_id}` - Obter veículo por ID
  - Query params: `films`, `pilots` (boolean)

### Favoritos (Requer Autenticação)

- `GET /favorites` - Listar todos os favoritos do usuário
- `GET /favorites/{type}` - Obter favorito por tipo
- `POST /favorites/{type}` - Adicionar favorito
  - Query params: `item_id`
- `DELETE /favorites/{type}` - Remover favorito
  - Query params: `item_id`

### Comentários (Requer Autenticação)

- `GET /comments` - Listar comentários
  - Query params: `item_id`, `item_type`
- `GET /comments/{comment_id}` - Obter comentário por ID
- `GET /comments/user/{user_id}` - Obter comentários de um usuário
- `POST /comments` - Criar comentário
- `PUT /comments/{comment_id}` - Atualizar comentário
- `DELETE /comments/{comment_id}` - Deletar comentário

## 🔐 Autenticação

A API utiliza autenticação JWT (JSON Web Tokens). Para acessar endpoints protegidos:

1. Registre-se em `/register`
2. Faça login em `/token` para obter o token
3. Use o token no header `Authorization: Bearer <seu-token>`

Exemplo:
```bash
curl -X GET http://localhost:8000/favorites \
  -H "Authorization: Bearer seu-token-aqui"
```

## 🐳 Docker

### Build da Imagem

```bash
docker build -t starwars-app -f Dockerfile .
```

### Executar com Docker Compose

```bash
# Iniciar todos os serviços
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar serviços
docker-compose down

# Parar e remover volumes
docker-compose down -v
```

O Docker Compose inicia automaticamente:
- **Aplicação FastAPI** na porta 8080
- **MongoDB** na porta 27017
- **Redis** na porta 6379

## 🧪 Testes

Execute os testes com pytest:

```bash
# Executar todos os testes
pytest

# Executar com verbosidade
pytest -v

# Executar teste específico
pytest test_main.py
```

## 📁 Estrutura do Projeto

```
starwars/
├── main.py                 # Aplicação principal FastAPI
├── config.py               # Configurações e variáveis de ambiente
├── strategy.py             # Funções de hash de senha e JWT
├── cache.py                # Funções de cache Redis
├── requirements.txt        # Dependências do projeto
├── Dockerfile              # Configuração Docker
├── compose.yml             # Docker Compose
├── test_main.py            # Testes principais
└── routers/
    ├── __init__.py
    ├── auth.py             # Rotas de autenticação
    ├── films.py            # Rotas de filmes
    ├── people.py           # Rotas de personagens
    ├── planets.py          # Rotas de planetas
    ├── species.py          # Rotas de espécies
    ├── starships.py        # Rotas de naves espaciais
    ├── vehicles.py         # Rotas de veículos
    ├── favorites.py        # Rotas de favoritos
    └── comments.py         # Rotas de comentários
```

## 🤝 Contribuindo

Contribuições são bem-vindas! Sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abrir um Pull Request

## 📝 Licença

Este projeto foi desenvolvido para fins de demonstração técnica.

## 👤 Autor

Desenvolvido como projeto técnico.

---

**Nota**: Esta API utiliza a [SWAPI](https://swapi.dev/) como fonte de dados. Todos os dados relacionados a Star Wars são propriedade da Lucasfilm Ltd.
