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
- [Deploy em Produção](#deploy-em-produção)
- [Testes](#testes)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Diagramas de Fluxo](#diagramas-de-fluxo)
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

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis. Você pode usar o arquivo `env.example` como referência:

```bash
cp env.example .env
```

Depois, edite o arquivo `.env` com suas credenciais:

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

**⚠️ Importante**: 
- Nunca commite o arquivo `.env` no repositório (já está no `.gitignore`)
- Para produção (Cloud Run), configure as variáveis de ambiente diretamente no serviço
- Se `MONGO_URI` não for fornecido, a aplicação construirá automaticamente a URI usando as outras variáveis do MongoDB

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

## ☁️ Deploy em Produção

A aplicação está hospedada em produção utilizando os seguintes serviços em nuvem:

### Infraestrutura

- **API**: Hospedada no [Google Cloud Run](https://cloud.google.com/run)
  - Serviço serverless totalmente gerenciado
  - Escalabilidade automática baseada em demanda
  - Deploy contínuo via container Docker
  
- **Banco de Dados**: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
  - Cluster gerenciado na nuvem
  - Alta disponibilidade e backup automático
  - Gerenciado via MongoDB Compass

- **Cache**: [Redis Cloud](https://redis.io/)
  - Instância gerenciada de Redis
  - Alta performance para operações de cache
  - Persistência de dados configurada

### Vantagens da Arquitetura em Nuvem

- **Escalabilidade**: A API escala automaticamente conforme a demanda
- **Alta Disponibilidade**: Serviços gerenciados garantem uptime elevado
- **Manutenção Simplificada**: Infraestrutura gerenciada reduz overhead operacional
- **Performance**: Cache Redis otimiza tempo de resposta
- **Segurança**: Serviços em nuvem oferecem recursos de segurança avançados

### Acessando a API em Produção

A API em produção está disponível através da URL do Cloud Run. Para acessar:

1. Use a URL fornecida pelo Google Cloud Run
2. A documentação interativa (Swagger) está disponível em `/docs`
3. Todos os endpoints funcionam da mesma forma que na versão local

**Nota**: As credenciais de produção são configuradas através de variáveis de ambiente no Cloud Run, garantindo segurança e flexibilidade.

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

## 📊 Diagramas de Fluxo

### Fluxo das Funções em `films.py`

O diagrama abaixo mostra o fluxo de execução de cada função no módulo `films.py`:

```mermaid
flowchart TD
    Start1[GET /films] --> CheckSearch{Parâmetro search?}
    CheckSearch -->|Sim| BuildSearchURL[Construir URL com search]
    CheckSearch -->|Não| BuildBaseURL[Usar URL base]
    BuildSearchURL --> FetchFilms[Fazer requisição HTTP para SWAPI]
    BuildBaseURL --> FetchFilms
    FetchFilms --> ParseJSON[Parsear resposta JSON]
    ParseJSON --> ValidateDetails[Chamar validate_details]
    
    ValidateDetails --> CheckSpecies{species = true?}
    CheckSpecies -->|Sim| GetSpecies[get_detailed_data para species]
    CheckSpecies -->|Não| CheckPeople{people = true?}
    GetSpecies --> CheckPeople
    CheckPeople -->|Sim| GetPeople[get_detailed_data para characters]
    CheckPeople -->|Não| CheckStarships{starships = true?}
    GetPeople --> CheckStarships
    CheckStarships -->|Sim| GetStarships[get_detailed_data para starships]
    CheckStarships -->|Não| CheckVehicles{vehicles = true?}
    GetStarships --> CheckVehicles
    CheckVehicles -->|Sim| GetVehicles[get_detailed_data para vehicles]
    CheckVehicles -->|Não| CheckPlanets{planets = true?}
    GetVehicles --> CheckPlanets
    CheckPlanets -->|Sim| GetPlanets[get_detailed_data para planets]
    CheckPlanets -->|Não| CreateResponse[Criar objeto search_films]
    GetPlanets --> CreateResponse
    
    CreateResponse --> CheckPagination{Resultados existem?}
    CheckPagination -->|Sim| ApplyPagination[Aplicar paginação: start_idx = page-1 * n, end_idx = page * n]
    CheckPagination -->|Não| CheckSorting{order_by definido?}
    ApplyPagination --> CheckSorting
    CheckSorting -->|Sim| ApplySorting[Ordenar por order_by com direção order_direction]
    CheckSorting -->|Não| ReturnFilms[Retornar resposta]
    ApplySorting --> ReturnFilms
    
    Start2["GET /films/film_id"] --> FetchFilm[Fazer requisição HTTP para SWAPI com film_id]
    FetchFilm --> ParseFilmJSON[Parsear resposta JSON]
    ParseFilmJSON --> ValidateFilmDetails[Chamar validate_details]
    ValidateFilmDetails --> CheckSpecies2{species = true?}
    CheckSpecies2 -->|Sim| GetSpecies2[get_detailed_data para species]
    CheckSpecies2 -->|Não| CheckPeople2{people = true?}
    GetSpecies2 --> CheckPeople2
    CheckPeople2 -->|Sim| GetPeople2[get_detailed_data para characters]
    CheckPeople2 -->|Não| CheckStarships2{starships = true?}
    GetPeople2 --> CheckStarships2
    CheckStarships2 -->|Sim| GetStarships2[get_detailed_data para starships]
    CheckStarships2 -->|Não| CheckVehicles2{vehicles = true?}
    CheckVehicles2 -->|Sim| GetVehicles2[get_detailed_data para vehicles]
    CheckVehicles2 -->|Não| CheckPlanets2{planets = true?}
    GetVehicles2 --> CheckPlanets2
    CheckPlanets2 -->|Sim| GetPlanets2[get_detailed_data para planets]
    CheckPlanets2 -->|Não| CreateFilmResponse[Criar objeto film]
    GetPlanets2 --> CreateFilmResponse
    CreateFilmResponse --> ReturnFilm[Retornar filme]
    
    Start3[get_detailed_data] --> CheckResults{results em data?}
    CheckResults -->|Sim| GetItems[Obter lista de items de results]
    CheckResults -->|Não| CreateSingleItem[Criar lista com data único]
    GetItems --> LoopFilms[Para cada filme em items]
    CreateSingleItem --> LoopFilms
    LoopFilms --> GetURLs[Obter lista de URLs do campo data]
    GetURLs --> LoopURLs[Para cada URL na lista]
    LoopURLs --> ExtractID[Extrair ID da URL: int do último segmento]
    ExtractID --> BuildCacheKey[Construir chave de cache: data/ID]
    BuildCacheKey --> CheckCache{Cache existe?}
    CheckCache -->|Sim| GetCached[Obter dados do cache]
    GetCached --> ParseCached[JSON.parse dos dados em cache]
    ParseCached --> AddCached[Adicionar aos detailed_data]
    CheckCache -->|Não| FetchData[Fazer requisição HTTP para SWAPI]
    FetchData --> CheckStatus{status_code = 200?}
    CheckStatus -->|Sim| ParseResponse[Parsear resposta JSON]
    ParseResponse --> AddData[Adicionar aos detailed_data]
    AddData --> SetCache[Salvar no cache com TTL 24h]
    CheckStatus -->|Não| AddURL[Adicionar URL original]
    SetCache --> CheckMoreURLs{Mais URLs?}
    AddURL --> CheckMoreURLs
    AddCached --> CheckMoreURLs
    CheckMoreURLs -->|Sim| LoopURLs
    CheckMoreURLs -->|Não| UpdateFilmItem[Atualizar film_item com detailed_data]
    UpdateFilmItem --> CheckMoreFilms{Mais filmes?}
    CheckMoreFilms -->|Sim| LoopFilms
    CheckMoreFilms -->|Não| EndGetDetailed[Retornar]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style ReturnFilms fill:#c8e6c9
    style ReturnFilm fill:#c8e6c9
    style EndGetDetailed fill:#c8e6c9
    style CheckCache fill:#fff9c4
    style CheckStatus fill:#fff9c4
```

### Legenda do Fluxo

- **Função `get_films`**: Endpoint principal que busca todos os filmes ou faz busca por título, com suporte a paginação, ordenação e expansão de dados relacionados.
- **Função `get_film`**: Endpoint que busca um filme específico por ID, com suporte a expansão de dados relacionados.
- **Função `get_detailed_data`**: Função auxiliar que expande URLs em dados completos, utilizando cache Redis para otimizar performance.
- **Função `validate_details`**: Função auxiliar que coordena a expansão de diferentes tipos de dados relacionados baseado nos parâmetros booleanos fornecidos.

### Fluxo das Funções em `people.py`

```mermaid
flowchart TD
    Start1[GET /people] --> CheckSearch{Parâmetro search?}
    CheckSearch -->|Sim| BuildSearchURL[Construir URL com search]
    CheckSearch -->|Não| BuildBaseURL[Usar URL base]
    BuildSearchURL --> FetchPeople[Fazer requisição HTTP para SWAPI]
    BuildBaseURL --> FetchPeople
    FetchPeople --> ParseJSON[Parsear resposta JSON]
    ParseJSON --> ValidateDetails[Chamar validate_details]
    
    ValidateDetails --> CheckFilms{films = true?}
    CheckFilms -->|Sim| GetFilms[get_detailed_data para films]
    CheckFilms -->|Não| CheckSpecies{species = true?}
    GetFilms --> CheckSpecies
    CheckSpecies -->|Sim| GetSpecies[get_detailed_data para species]
    CheckSpecies -->|Não| CheckStarships{starships = true?}
    GetSpecies --> CheckStarships
    CheckStarships -->|Sim| GetStarships[get_detailed_data para starships]
    CheckStarships -->|Não| CheckVehicles{vehicles = true?}
    GetStarships --> CheckVehicles
    CheckVehicles -->|Sim| GetVehicles[get_detailed_data para vehicles]
    CheckVehicles -->|Não| CheckHomeworld{homeworld = true?}
    GetVehicles --> CheckHomeworld
    CheckHomeworld -->|Sim| GetHomeworld[get_detailed_data para homeworld]
    CheckHomeworld -->|Não| CreateResponse[Criar objeto search_people]
    GetHomeworld --> CreateResponse
    
    CreateResponse --> CheckPagination{Resultados existem?}
    CheckPagination -->|Sim| ApplyPagination[Aplicar paginação]
    CheckPagination -->|Não| CheckSorting{order_by definido?}
    ApplyPagination --> CheckSorting
    CheckSorting -->|Sim| ApplySorting[Ordenar resultados]
    CheckSorting -->|Não| ReturnPeople[Retornar resposta]
    ApplySorting --> ReturnPeople
    
    Start2["GET /people/person_id"] --> FetchPerson[Fazer requisição HTTP para SWAPI com person_id]
    FetchPerson --> ParsePersonJSON[Parsear resposta JSON]
    ParsePersonJSON --> WrapResults[Envolver em results: array]
    WrapResults --> ValidatePersonDetails[Chamar validate_details]
    ValidatePersonDetails --> CheckFilms2{films = true?}
    CheckFilms2 -->|Sim| GetFilms2[get_detailed_data para films]
    CheckFilms2 -->|Não| CheckSpecies2{species = true?}
    GetFilms2 --> CheckSpecies2
    CheckSpecies2 -->|Sim| GetSpecies2[get_detailed_data para species]
    CheckSpecies2 -->|Não| CheckStarships2{starships = true?}
    GetSpecies2 --> CheckStarships2
    CheckStarships2 -->|Sim| GetStarships2[get_detailed_data para starships]
    CheckStarships2 -->|Não| CheckVehicles2{vehicles = true?}
    GetStarships2 --> CheckVehicles2
    CheckVehicles2 -->|Sim| GetVehicles2[get_detailed_data para vehicles]
    CheckVehicles2 -->|Não| CheckHomeworld2{homeworld = true?}
    GetVehicles2 --> CheckHomeworld2
    CheckHomeworld2 -->|Sim| GetHomeworld2[get_detailed_data para homeworld]
    CheckHomeworld2 -->|Não| CreatePersonResponse[Criar objeto person]
    GetHomeworld2 --> CreatePersonResponse
    CreatePersonResponse --> ReturnPerson[Retornar personagem]
    
    Start3[get_detailed_data people] --> CheckResults{results em data?}
    CheckResults -->|Sim| GetItems[Obter lista de items de results]
    CheckResults -->|Não| CreateSingleItem[Criar lista com data único]
    GetItems --> LoopPeople[Para cada personagem em items]
    CreateSingleItem --> LoopPeople
    LoopPeople --> CheckHomeworldField{data = homeworld?}
    CheckHomeworldField -->|Sim| GetHomeworldURL[Obter URL única de homeworld]
    GetHomeworldURL --> ExtractPlanetID[Extrair ID do planeta]
    ExtractPlanetID --> BuildPlanetCacheKey[Construir chave: planets/ID]
    BuildPlanetCacheKey --> CheckPlanetCache{Cache existe?}
    CheckPlanetCache -->|Sim| GetPlanetCached[Obter planeta do cache]
    GetPlanetCached --> ParsePlanetCached[JSON.parse]
    ParsePlanetCached --> UpdateHomeworld[Atualizar person_item homeworld]
    CheckPlanetCache -->|Não| FetchPlanet[Fazer requisição para planets/ID]
    FetchPlanet --> CheckPlanetStatus{status_code = 200?}
    CheckPlanetStatus -->|Sim| UpdateHomeworld
    CheckPlanetStatus -->|Não| KeepURL[Manter URL original]
    UpdateHomeworld --> CheckMorePeople{Mais personagens?}
    KeepURL --> CheckMorePeople
    
    CheckHomeworldField -->|Não| GetURLs[Obter lista de URLs]
    GetURLs --> NormalizeURLs{URLs é string?}
    NormalizeURLs -->|Sim| ConvertToList[Converter para lista]
    NormalizeURLs -->|Não| CheckNull{URLs é None?}
    CheckNull -->|Sim| EmptyList[Lista vazia]
    CheckNull -->|Não| LoopURLs[Para cada URL]
    ConvertToList --> LoopURLs
    EmptyList --> CheckMorePeople
    LoopURLs --> ExtractID[Extrair ID da URL]
    ExtractID --> BuildCacheKey[Construir chave de cache]
    BuildCacheKey --> CheckCache{Cache existe?}
    CheckCache -->|Sim| GetCached[Obter dados do cache]
    GetCached --> ParseCached[JSON.parse]
    ParseCached --> AddCached[Adicionar aos detailed_data]
    CheckCache -->|Não| FetchData[Fazer requisição HTTP]
    FetchData --> CheckStatus{status_code = 200?}
    CheckStatus -->|Sim| ParseResponse[Parsear resposta]
    ParseResponse --> AddData[Adicionar aos detailed_data]
    AddData --> SetCache[Salvar no cache TTL 24h]
    CheckStatus -->|Não| AddURL[Adicionar URL original]
    SetCache --> CheckMoreURLs{Mais URLs?}
    AddURL --> CheckMoreURLs
    AddCached --> CheckMoreURLs
    CheckMoreURLs -->|Sim| LoopURLs
    CheckMoreURLs -->|Não| UpdatePersonItem[Atualizar person_item]
    UpdatePersonItem --> CheckMorePeople
    CheckMorePeople -->|Sim| LoopPeople
    CheckMorePeople -->|Não| EndGetDetailed[Retornar]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style ReturnPeople fill:#c8e6c9
    style ReturnPerson fill:#c8e6c9
    style EndGetDetailed fill:#c8e6c9
```

#### Legenda do Fluxo - `people.py`

- **Função `get_people`**: Endpoint principal que busca todos os personagens ou faz busca por nome, com suporte a paginação, ordenação e expansão de dados relacionados (filmes, espécies, naves, veículos, planeta natal).
- **Função `get_person`**: Endpoint que busca um personagem específico por ID, com suporte a expansão de dados relacionados. Envolve os dados em uma estrutura `results` para compatibilidade com `validate_details`.
- **Função `get_detailed_data`**: Função auxiliar que expande URLs em dados completos, com tratamento especial para `homeworld` (que é uma URL única, não uma lista) e normalização de URLs que podem ser strings, listas ou None. Utiliza cache Redis para otimizar performance.
- **Função `validate_details`**: Função auxiliar que coordena a expansão de diferentes tipos de dados relacionados baseado nos parâmetros booleanos fornecidos (films, species, starships, vehicles, homeworld).

### Fluxo das Funções em `planets.py`

```mermaid
flowchart TD
    Start1[GET /planets] --> CheckSearch{Parâmetro search?}
    CheckSearch -->|Sim| BuildSearchURL[Construir URL com search]
    CheckSearch -->|Não| BuildBaseURL[Usar URL base]
    BuildSearchURL --> FetchPlanets[Fazer requisição HTTP para SWAPI]
    BuildBaseURL --> FetchPlanets
    FetchPlanets --> ParseJSON[Parsear resposta JSON]
    ParseJSON --> ValidateDetails[Chamar validate_details]
    
    ValidateDetails --> CheckResidents{residents = true?}
    CheckResidents -->|Sim| GetResidents[get_detailed_data para residents]
    CheckResidents -->|Não| CheckFilms{films = true?}
    GetResidents --> CheckFilms
    CheckFilms -->|Sim| GetFilms[get_detailed_data para films]
    CheckFilms -->|Não| CreateResponse[Criar objeto search_planets]
    GetFilms --> CreateResponse
    
    CreateResponse --> CheckPagination{Resultados existem?}
    CheckPagination -->|Sim| ApplyPagination[Aplicar paginação]
    CheckPagination -->|Não| CheckSorting{order_by definido?}
    ApplyPagination --> CheckSorting
    CheckSorting -->|Sim| ApplySorting[Ordenar resultados]
    CheckSorting -->|Não| ReturnPlanets[Retornar resposta]
    ApplySorting --> ReturnPlanets
    
    Start2["GET /planets/planet_id"] --> FetchPlanet[Fazer requisição HTTP para SWAPI com planet_id]
    FetchPlanet --> ParsePlanetJSON[Parsear resposta JSON]
    ParsePlanetJSON --> ValidatePlanetDetails[Chamar validate_details]
    ValidatePlanetDetails --> CheckResidents2{residents = true?}
    CheckResidents2 -->|Sim| GetResidents2[get_detailed_data para residents]
    CheckResidents2 -->|Não| CheckFilms2{films = true?}
    GetResidents2 --> CheckFilms2
    CheckFilms2 -->|Sim| GetFilms2[get_detailed_data para films]
    CheckFilms2 -->|Não| CreatePlanetResponse[Criar objeto planet]
    GetFilms2 --> CreatePlanetResponse
    CreatePlanetResponse --> ReturnPlanet[Retornar planeta]
    
    Start3[get_detailed_data planets] --> CheckResults{results em data?}
    CheckResults -->|Sim| GetItems[Obter lista de items de results]
    CheckResults -->|Não| CreateSingleItem[Criar lista com data único]
    GetItems --> LoopPlanets[Para cada planeta em items]
    CreateSingleItem --> LoopPlanets
    LoopPlanets --> CheckResidentsField{data = residents?}
    CheckResidentsField -->|Sim| SetFieldName[field_name = people]
    CheckResidentsField -->|Não| SetFieldName2[field_name = data]
    SetFieldName --> GetURLs[Obter URLs do campo data]
    SetFieldName2 --> GetURLs
    GetURLs --> NormalizeURLs{URLs é string?}
    NormalizeURLs -->|Sim| ConvertToList[Converter para lista]
    NormalizeURLs -->|Não| LoopURLs[Para cada URL]
    ConvertToList --> LoopURLs
    LoopURLs --> ExtractID[Extrair ID da URL]
    ExtractID --> BuildCacheKey[Construir chave: field_name/ID]
    BuildCacheKey --> CheckCache{Cache existe?}
    CheckCache -->|Sim| GetCached[Obter dados do cache]
    GetCached --> ParseCached[JSON.parse]
    ParseCached --> AddCached[Adicionar aos detailed_data]
    CheckCache -->|Não| FetchData[Fazer requisição HTTP]
    FetchData --> CheckStatus{status_code = 200?}
    CheckStatus -->|Sim| ParseResponse[Parsear resposta]
    ParseResponse --> AddData[Adicionar aos detailed_data]
    AddData --> SetCache[Salvar no cache TTL 24h]
    CheckStatus -->|Não| AddURL[Adicionar URL original]
    SetCache --> CheckMoreURLs{Mais URLs?}
    AddURL --> CheckMoreURLs
    AddCached --> CheckMoreURLs
    CheckMoreURLs -->|Sim| LoopURLs
    CheckMoreURLs -->|Não| UpdatePlanetItem[Atualizar planet_item]
    UpdatePlanetItem --> CheckMorePlanets{Mais planetas?}
    CheckMorePlanets -->|Sim| LoopPlanets
    CheckMorePlanets -->|Não| EndGetDetailed[Retornar]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style ReturnPlanets fill:#c8e6c9
    style ReturnPlanet fill:#c8e6c9
    style EndGetDetailed fill:#c8e6c9
```

#### Legenda do Fluxo - `planets.py`

- **Função `get_planets`**: Endpoint principal que busca todos os planetas ou faz busca por nome, com suporte a paginação, ordenação e expansão de dados relacionados (residentes, filmes).
- **Função `get_planet`**: Endpoint que busca um planeta específico por ID, com suporte a expansão de dados relacionados.
- **Função `get_detailed_data`**: Função auxiliar que expande URLs em dados completos, com mapeamento especial para `residents` (que mapeia para o endpoint `people` da SWAPI). Normaliza URLs que podem ser strings ou listas. Utiliza cache Redis para otimizar performance.
- **Função `validate_details`**: Função auxiliar que coordena a expansão de diferentes tipos de dados relacionados baseado nos parâmetros booleanos fornecidos (residents, films).

### Fluxo das Funções em `auth.py`

```mermaid
flowchart TD
    Start1[POST /register] --> GetUserData[Receber dados do usuário]
    GetUserData --> HashPassword[Hash da senha com bcrypt]
    HashPassword --> CheckUserExists{Usuário já existe?}
    CheckUserExists -->|Sim| ReturnError[Retornar erro 400]
    CheckUserExists -->|Não| InsertUser[Inserir usuário no MongoDB]
    InsertUser --> ReturnSuccess[Retornar mensagem de sucesso]
    
    Start2[POST /token] --> GetFormData[Receber form_data OAuth2]
    GetFormData --> FindUser[Buscar usuário no MongoDB]
    FindUser --> CheckUserFound{Usuário encontrado?}
    CheckUserFound -->|Não| ReturnAuthError[Retornar erro 400]
    CheckUserFound -->|Sim| VerifyPassword[Verificar senha com bcrypt]
    VerifyPassword --> CheckPasswordValid{Senha válida?}
    CheckPasswordValid -->|Não| ReturnAuthError
    CheckPasswordValid -->|Sim| CreateToken[Criar JWT token]
    CreateToken --> ReturnToken[Retornar access_token e token_type]
    
    Start3[get_current_user] --> ExtractToken[Extrair token do header]
    ExtractToken --> DecodeToken[Decodificar JWT token]
    DecodeToken --> CheckDecodeValid{Decodificação válida?}
    CheckDecodeValid -->|Não| Return401Error[Retornar erro 401]
    CheckDecodeValid -->|Sim| ExtractUsername[Extrair username do payload]
    ExtractUsername --> ExtractUserID[Extrair user_id do payload]
    ExtractUserID --> CheckUsername{username existe?}
    CheckUsername -->|Não| Return401Error
    CheckUsername -->|Sim| ReturnUser[Retornar dict com username e id]
    
    Start4[DELETE /user] --> GetCurrentUser[Obter usuário atual via get_current_user]
    GetCurrentUser --> ConvertToObjectId[Converter user_id para ObjectId]
    ConvertToObjectId --> DeleteUser[Deletar usuário do MongoDB]
    DeleteUser --> ReturnDeleteSuccess[Retornar mensagem de sucesso]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style Start4 fill:#e1f5ff
    style ReturnSuccess fill:#c8e6c9
    style ReturnToken fill:#c8e6c9
    style ReturnUser fill:#c8e6c9
    style ReturnDeleteSuccess fill:#c8e6c9
    style ReturnError fill:#ffcdd2
    style ReturnAuthError fill:#ffcdd2
    style Return401Error fill:#ffcdd2
```

#### Legenda do Fluxo - `auth.py`

- **Função `register`**: Endpoint que registra um novo usuário. Faz hash da senha com bcrypt, verifica se o usuário já existe e insere no MongoDB.
- **Função `login`**: Endpoint que autentica um usuário e retorna um token JWT. Utiliza OAuth2PasswordRequestForm para receber credenciais, verifica usuário e senha no MongoDB, e gera token com username e user_id.
- **Função `get_current_user`**: Função de dependência que valida o token JWT, extrai informações do payload (username e id) e retorna um dicionário com os dados do usuário autenticado. Usado como `Depends()` em endpoints protegidos.
- **Função `delete_user`**: Endpoint protegido que deleta o usuário autenticado do MongoDB, convertendo o user_id para ObjectId.

### Fluxo das Funções em `favorites.py`

```mermaid
flowchart TD
    Start1[GET /favorites] --> Authenticate[Autenticar via get_current_user]
    Authenticate --> ExtractUserID[Extrair user_id do token]
    ExtractUserID --> QueryFavorites[Buscar favoritos no MongoDB]
    QueryFavorites --> ConvertObjectIds[Converter ObjectIds para strings]
    ConvertObjectIds --> ReturnFavorites[Retornar lista de favoritos]
    
    Start2["GET /favorites/type"] --> Authenticate2[Autenticar via get_current_user]
    Authenticate2 --> ExtractUserID2[Extrair user_id do token]
    ExtractUserID2 --> QueryFavorite[Buscar favorito por type e user_id]
    QueryFavorite --> ConvertObjectId[Converter ObjectId para string]
    ConvertObjectId --> ReturnFavorite[Retornar favorito]
    
    Start3["POST /favorites/type"] --> Authenticate3[Autenticar via get_current_user]
    Authenticate3 --> ExtractUserID3[Extrair user_id do token]
    ExtractUserID3 --> GetItemID[Obter item_id dos parâmetros]
    GetItemID --> CheckFavoriteExists{ favorito já existe?}
    CheckFavoriteExists -->|Sim| Return400Error[Retornar erro 400]
    CheckFavoriteExists -->|Não| InsertFavorite[Inserir favorito no MongoDB]
    InsertFavorite --> ReturnAddSuccess[Retornar mensagem de sucesso]
    
    Start4["DELETE /favorites/type"] --> Authenticate4[Autenticar via get_current_user]
    Authenticate4 --> ExtractUserID4[Extrair user_id do token]
    ExtractUserID4 --> GetItemID2[Obter item_id dos parâmetros]
    GetItemID2 --> DeleteFavorite[Deletar favorito do MongoDB]
    DeleteFavorite --> ReturnDeleteSuccess[Retornar mensagem de sucesso]
    
    Start5[convert_objectid_to_str] --> CheckDocNone{doc é None?}
    CheckDocNone -->|Sim| ReturnNone[Retornar None]
    CheckDocNone -->|Não| CheckIsDict{é dict?}
    CheckIsDict -->|Não| ReturnDoc[Retornar doc]
    CheckIsDict -->|Sim| LoopKeys[Para cada chave no dict]
    LoopKeys --> CheckValueObjectId{valor é ObjectId?}
    CheckValueObjectId -->|Sim| ConvertToString[str do ObjectId]
    CheckValueObjectId -->|Não| CheckValueDict{valor é dict?}
    ConvertToString --> AddToResult[Adicionar ao resultado]
    CheckValueDict -->|Sim| RecursiveConvert[Chamar recursivamente]
    CheckValueDict -->|Não| CheckValueList{valor é list?}
    RecursiveConvert --> AddToResult
    CheckValueList -->|Sim| LoopListItems[Para cada item na lista]
    LoopListItems --> CheckItemConvert{item é dict ou ObjectId?}
    CheckItemConvert -->|Sim| ConvertItem[Converter item]
    CheckItemConvert -->|Não| KeepItem[Manter item]
    ConvertItem --> AddToList[Adicionar à lista convertida]
    KeepItem --> AddToList
    AddToList --> CheckMoreItems{Mais itens?}
    CheckMoreItems -->|Sim| LoopListItems
    CheckMoreItems -->|Não| AddToResult
    CheckValueList -->|Não| AddToResult
    AddToResult --> CheckMoreKeys{Mais chaves?}
    CheckMoreKeys -->|Sim| LoopKeys
    CheckMoreKeys -->|Não| ReturnResult[Retornar resultado]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style Start4 fill:#e1f5ff
    style Start5 fill:#e1f5ff
    style ReturnFavorites fill:#c8e6c9
    style ReturnFavorite fill:#c8e6c9
    style ReturnAddSuccess fill:#c8e6c9
    style ReturnDeleteSuccess fill:#c8e6c9
    style ReturnResult fill:#c8e6c9
    style Return400Error fill:#ffcdd2
```

#### Legenda do Fluxo - `favorites.py`

- **Função `get_favorites`**: Endpoint protegido que retorna todos os favoritos do usuário autenticado. Busca no MongoDB usando o user_id extraído do token JWT.
- **Função `get_favorite`**: Endpoint protegido que retorna um favorito específico por tipo. Busca no MongoDB usando user_id e type.
- **Função `add_favorite`**: Endpoint protegido que adiciona um novo favorito. Verifica se já existe um favorito do mesmo tipo para o usuário antes de inserir.
- **Função `delete_favorite`**: Endpoint protegido que remove um favorito específico usando user_id, type e item_id.
- **Função `convert_objectid_to_str`**: Função auxiliar recursiva que converte todos os ObjectIds de um documento MongoDB para strings, permitindo serialização JSON correta. Trata dicts, listas e valores aninhados.

### Fluxo das Funções em `comments.py`

```mermaid
flowchart TD
    Start1[POST /comments] --> Authenticate[Autenticar via get_current_user]
    Authenticate --> GetCommentData[Receber dados do comentário]
    GetCommentData --> GetCurrentTime[Obter timestamp atual]
    GetCurrentTime --> ConvertUserID[Converter user_id para ObjectId]
    ConvertUserID --> InsertComment[Inserir comentário no MongoDB]
    InsertComment --> ReturnSuccess[Retornar mensagem de sucesso]
    
    Start2[GET /comments] --> GetQueryParams[Obter item_id, item_type, page, limit]
    GetQueryParams --> BuildQuery[Construir query MongoDB]
    BuildQuery --> ApplySkipLimit[Aplicar skip e limit]
    ApplySkipLimit --> CheckOrderBy{order_by definido?}
    CheckOrderBy -->|Sim| SortComments[Ordenar comentários]
    CheckOrderBy -->|Não| ConvertObjectIds[Converter ObjectIds para strings]
    SortComments --> ConvertObjectIds
    ConvertObjectIds --> CountTotal[Contar total de documentos]
    CountTotal --> ReturnComments[Retornar comments_response]
    
    Start3["GET /comments/comment_id"] --> ConvertToObjectId[Converter comment_id para ObjectId]
    ConvertToObjectId --> FindComment[Buscar comentário no MongoDB]
    FindComment --> CheckFound{Comentário encontrado?}
    CheckFound -->|Não| Return404Error[Retornar erro 404]
    CheckFound -->|Sim| ConvertObjectId[Converter ObjectId para string]
    ConvertObjectId --> ReturnComment[Retornar comentário]
    
    Start4["GET /comments/user/user_id"] --> ConvertUserID2[Converter user_id para ObjectId]
    ConvertUserID2 --> BuildUserQuery[Construir query por user_id]
    BuildUserQuery --> ApplySkipLimit2[Aplicar skip e limit]
    ApplySkipLimit2 --> CheckOrderBy2{order_by definido?}
    CheckOrderBy2 -->|Sim| SortComments2[Ordenar comentários]
    CheckOrderBy2 -->|Não| ConvertObjectIds2[Converter ObjectIds]
    SortComments2 --> ConvertObjectIds2
    ConvertObjectIds2 --> CountTotal2[Contar total]
    CountTotal2 --> ReturnUserComments[Retornar comments_response]
    
    Start5["PUT /comments/comment_id"] --> Authenticate2[Autenticar via get_current_user]
    Authenticate2 --> GetUpdateData[Receber dados de atualização]
    GetUpdateData --> GetCurrentTime2[Obter timestamp atual]
    GetCurrentTime2 --> ConvertCommentID[Converter comment_id para ObjectId]
    ConvertCommentID --> ConvertUserID3[Converter user_id para ObjectId]
    ConvertUserID3 --> UpdateComment[Atualizar comentário no MongoDB]
    UpdateComment --> CheckMatched{matched_count > 0?}
    CheckMatched -->|Não| Return404Error2[Retornar erro 404]
    CheckMatched -->|Sim| ReturnUpdateSuccess[Retornar mensagem de sucesso]
    
    Start6["DELETE /comments/comment_id"] --> Authenticate3[Autenticar via get_current_user]
    Authenticate3 --> ConvertCommentID2[Converter comment_id para ObjectId]
    ConvertCommentID2 --> ConvertUserID4[Converter user_id para ObjectId]
    ConvertUserID4 --> DeleteComment[Deletar comentário do MongoDB]
    DeleteComment --> CheckDeleted{deleted_count > 0?}
    CheckDeleted -->|Não| Return404Error3[Retornar erro 404]
    CheckDeleted -->|Sim| ReturnDeleteSuccess[Retornar mensagem de sucesso]
    
    Start7[convert_objectid_to_str] --> CheckDocNone{doc é None?}
    CheckDocNone -->|Sim| ReturnNone[Retornar None]
    CheckDocNone -->|Não| CheckIsDict{é dict?}
    CheckIsDict -->|Não| ReturnDoc[Retornar doc]
    CheckIsDict -->|Sim| LoopKeys[Para cada chave no dict]
    LoopKeys --> CheckValueObjectId{valor é ObjectId?}
    CheckValueObjectId -->|Sim| ConvertToString[str do ObjectId]
    CheckValueObjectId -->|Não| CheckValueDict{valor é dict?}
    ConvertToString --> AddToResult[Adicionar ao resultado]
    CheckValueDict -->|Sim| RecursiveConvert[Chamar recursivamente]
    CheckValueDict -->|Não| CheckValueList{valor é list?}
    RecursiveConvert --> AddToResult
    CheckValueList -->|Sim| LoopListItems[Para cada item na lista]
    LoopListItems --> CheckItemConvert{item é dict ou ObjectId?}
    CheckItemConvert -->|Sim| ConvertItem[Converter item]
    CheckItemConvert -->|Não| KeepItem[Manter item]
    ConvertItem --> AddToList[Adicionar à lista convertida]
    KeepItem --> AddToList
    AddToList --> CheckMoreItems{Mais itens?}
    CheckMoreItems -->|Sim| LoopListItems
    CheckMoreItems -->|Não| AddToResult
    CheckValueList -->|Não| AddToResult
    AddToResult --> CheckMoreKeys{Mais chaves?}
    CheckMoreKeys -->|Sim| LoopKeys
    CheckMoreKeys -->|Não| ReturnResult[Retornar resultado]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style Start4 fill:#e1f5ff
    style Start5 fill:#e1f5ff
    style Start6 fill:#e1f5ff
    style Start7 fill:#e1f5ff
    style ReturnSuccess fill:#c8e6c9
    style ReturnComments fill:#c8e6c9
    style ReturnComment fill:#c8e6c9
    style ReturnUserComments fill:#c8e6c9
    style ReturnUpdateSuccess fill:#c8e6c9
    style ReturnDeleteSuccess fill:#c8e6c9
    style ReturnResult fill:#c8e6c9
    style Return404Error fill:#ffcdd2
    style Return404Error2 fill:#ffcdd2
    style Return404Error3 fill:#ffcdd2
```

#### Legenda do Fluxo - `comments.py`

- **Função `add_comment`**: Endpoint protegido que cria um novo comentário. Adiciona timestamp de criação e associa o comentário ao user_id do usuário autenticado.
- **Função `get_comments`**: Endpoint que retorna comentários filtrados por item_id e item_type, com suporte a paginação (page, limit) e ordenação opcional.
- **Função `get_comment`**: Endpoint que retorna um comentário específico por ID. Retorna erro 404 se não encontrado.
- **Função `get_comments_by_user`**: Endpoint que retorna todos os comentários de um usuário específico, com suporte a paginação e ordenação.
- **Função `update_comment`**: Endpoint protegido que atualiza um comentário. Verifica se o comentário pertence ao usuário autenticado antes de atualizar. Adiciona timestamp de atualização.
- **Função `delete_comment`**: Endpoint protegido que deleta um comentário. Verifica se o comentário pertence ao usuário autenticado antes de deletar. Retorna erro 404 se não encontrado ou sem permissão.
- **Função `convert_objectid_to_str`**: Função auxiliar recursiva que converte todos os ObjectIds de um documento MongoDB para strings, permitindo serialização JSON correta. Trata dicts, listas e valores aninhados.

### Fluxo das Funções em `vehicles.py` e `starships.py`

```mermaid
flowchart TD
    Start1[GET /vehicles ou GET /starships] --> CheckSearch{Parâmetro search?}
    CheckSearch -->|Sim| BuildSearchURL[Construir URL com search]
    CheckSearch -->|Não| BuildBaseURL[Usar URL base]
    BuildSearchURL --> FetchData[Fazer requisição HTTP para SWAPI]
    BuildBaseURL --> FetchData
    FetchData --> ParseJSON[Parsear resposta JSON]
    ParseJSON --> ValidateDetails[Chamar validate_details]
    
    ValidateDetails --> CheckFilms{films = true?}
    CheckFilms -->|Sim| GetFilms[get_detailed_data para films]
    CheckFilms -->|Não| CheckPilots{pilots = true?}
    GetFilms --> CheckPilots
    CheckPilots -->|Sim| GetPilots[get_detailed_data para pilots]
    CheckPilots -->|Não| CreateResponse[Criar objeto search_vehicles/starships]
    GetPilots --> CreateResponse
    
    CreateResponse --> CheckPagination{Resultados existem?}
    CheckPagination -->|Sim| ApplyPagination[Aplicar paginação]
    CheckPagination -->|Não| CheckSorting{order_by definido?}
    ApplyPagination --> CheckSorting
    CheckSorting -->|Sim| ApplySorting[Ordenar resultados]
    CheckSorting -->|Não| ReturnData[Retornar resposta]
    ApplySorting --> ReturnData
    
    Start2["GET /vehicles/vehicle_id ou GET /starships/starship_id"] --> FetchItem[Fazer requisição HTTP para SWAPI com ID]
    FetchItem --> ParseItemJSON[Parsear resposta JSON]
    ParseItemJSON --> ValidateItemDetails[Chamar validate_details]
    ValidateItemDetails --> CheckFilms2{films = true?}
    CheckFilms2 -->|Sim| GetFilms2[get_detailed_data para films]
    CheckFilms2 -->|Não| CheckPilots2{pilots = true?}
    GetFilms2 --> CheckPilots2
    CheckPilots2 -->|Sim| GetPilots2[get_detailed_data para pilots]
    CheckPilots2 -->|Não| CreateItemResponse[Criar objeto vehicle/starship]
    GetPilots2 --> CreateItemResponse
    CreateItemResponse --> ReturnItem[Retornar veículo/nave]
    
    Start3[get_detailed_data vehicles/starships] --> CheckResults{results em data?}
    CheckResults -->|Sim| GetItems[Obter lista de items de results]
    CheckResults -->|Não| CreateSingleItem[Criar lista com data único]
    GetItems --> LoopItems[Para cada item em items]
    CreateSingleItem --> LoopItems
    LoopItems --> GetURLs[Obter URLs do campo data]
    GetURLs --> CheckURLsNull{URLs é None?}
    CheckURLsNull -->|Sim| EmptyList[Lista vazia]
    CheckURLsNull -->|Não| CheckURLsString{URLs é string?}
    CheckURLsString -->|Sim| ConvertToList[Converter para lista]
    CheckURLsString -->|Não| LoopURLs[Para cada URL]
    ConvertToList --> LoopURLs
    EmptyList --> CheckPilotsField{data = pilots?}
    CheckPilotsField -->|Sim| SetFieldName[field_name = people]
    CheckPilotsField -->|Não| SetFieldName2[field_name = data]
    SetFieldName --> LoopURLs
    SetFieldName2 --> LoopURLs
    LoopURLs --> ExtractID[Extrair ID da URL]
    ExtractID --> BuildCacheKey[Construir chave: field_name/ID]
    BuildCacheKey --> CheckCache{Cache existe?}
    CheckCache -->|Sim| GetCached[Obter dados do cache]
    GetCached --> ParseCached[JSON.parse]
    ParseCached --> AddCached[Adicionar aos detailed_data]
    CheckCache -->|Não| FetchData2[Fazer requisição HTTP]
    FetchData2 --> CheckStatus{status_code = 200?}
    CheckStatus -->|Sim| ParseResponse[Parsear resposta]
    ParseResponse --> AddData[Adicionar aos detailed_data]
    AddData --> SetCache[Salvar no cache TTL 24h]
    CheckStatus -->|Não| AddURL[Adicionar URL original]
    SetCache --> CheckMoreURLs{Mais URLs?}
    AddURL --> CheckMoreURLs
    AddCached --> CheckMoreURLs
    CheckMoreURLs -->|Sim| LoopURLs
    CheckMoreURLs -->|Não| UpdateItem[Atualizar item com detailed_data]
    UpdateItem --> CheckMoreItems{Mais itens?}
    CheckMoreItems -->|Sim| LoopItems
    CheckMoreItems -->|Não| EndGetDetailed[Retornar]
    
    style Start1 fill:#e1f5ff
    style Start2 fill:#e1f5ff
    style Start3 fill:#e1f5ff
    style ReturnData fill:#c8e6c9
    style ReturnItem fill:#c8e6c9
    style EndGetDetailed fill:#c8e6c9
```

#### Legenda do Fluxo - `vehicles.py` e `starships.py`

- **Função `get_vehicles` / `get_starships`**: Endpoints principais que buscam todos os veículos ou naves espaciais, com suporte a busca por nome/modelo, paginação, ordenação e expansão de dados relacionados (filmes, pilotos).
- **Função `get_vehicle` / `get_starship`**: Endpoints que buscam um veículo ou nave espacial específico por ID, com suporte a expansão de dados relacionados.
- **Função `get_detailed_data`**: Função auxiliar que expande URLs em dados completos, com mapeamento especial para `pilots` (que mapeia para o endpoint `people` da SWAPI). Normaliza URLs que podem ser strings, listas ou None. Utiliza cache Redis para otimizar performance.
- **Função `validate_details`**: Função auxiliar que coordena a expansão de diferentes tipos de dados relacionados baseado nos parâmetros booleanos fornecidos (films, pilots).

## 📝 Licença

Este projeto foi desenvolvido para fins de demonstração técnica.

## 👤 Autor

[Pedro Jorge Zampieri Silva](https://github.com/pedrozampi/)

---

**Nota**: Esta API utiliza a [SWAPI](https://swapi.dev/) como fonte de dados. Todos os dados relacionados a Star Wars são propriedade da Lucasfilm Ltd.
