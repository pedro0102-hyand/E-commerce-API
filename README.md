# 🛒 E-commerce API

API RESTful completa para e-commerce desenvolvida com **FastAPI**, **SQLAlchemy** e **SQLite**. Sistema robusto com autenticação JWT, gerenciamento de produtos, carrinho de compras e processamento de pedidos.

---

## ✨ Funcionalidades

### 🔐 Autenticação e Autorização
- Registro de usuários com validação de e-mail
- Login com geração de token JWT
- Proteção de rotas por autenticação
- Sistema de permissões (Usuário comum vs Admin)
- Rate limiting para prevenir ataques de força bruta

### 📦 Gerenciamento de Produtos
- **CRUD completo** (Create, Read, Update, Delete)
- Controle de estoque em tempo real
- Validação de dados com Pydantic
- Acesso restrito (apenas admins podem criar/editar)

### 🛒 Carrinho de Compras
- Adicionar produtos ao carrinho
- Atualização automática de quantidades
- Validação de estoque antes da adição
- Cálculo automático do total

### 💳 Checkout e Pagamentos
- Finalização de pedidos
- Simulação de processamento de pagamento
- Baixa automática de estoque após confirmação
- Geração de referência de pagamento (UUID)

### 📊 Gestão de Pedidos
- Consulta de histórico de pedidos por usuário
- Detalhamento completo de cada pedido
- Painel administrativo (visualização de todos os pedidos)
- Estados de pedido: `CART`, `PENDING_PAYMENT`, `PAID`, `CANCELLED`

---

## 🚀 Tecnologias Utilizadas

| Categoria | Tecnologia |
|-----------|-----------|
| **Framework Web** | FastAPI 0.104+ |
| **Servidor ASGI** | Uvicorn |
| **ORM** | SQLAlchemy 2.0+ |
| **Banco de Dados** | SQLite 3 |
| **Validação de Dados** | Pydantic V2 |
| **Autenticação** | JWT (python-jose) |
| **Criptografia** | Passlib + Bcrypt |
| **Rate Limiting** | SlowAPI |
| **Testes** | Pytest |

---

## 📂 Arquitetura do Projeto

```
ecommerce-api/
├── app/
│   ├── __init__.py
│   ├── main.py                    # Ponto de entrada da aplicação
│   ├── config.py                  # Configurações e variáveis de ambiente
│   ├── database.py                # Conexão com banco de dados
│   ├── utils.py                   # Utilitários (rate limiter)
│   │
│   ├── auth/                      # Módulo de autenticação
│   │   ├── dependencies.py        # Dependências de autenticação
│   │   ├── jwt.py                 # Criação e validação de tokens
│   │   └── security.py            # Hashing de senhas
│   │
│   ├── models/                    # Modelos ORM (tabelas do banco)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── order.py
│   │   ├── order_item.py
│   │   └── order_status.py
│   │
│   ├── schemas/                   # Schemas Pydantic (validação)
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── cart.py
│   │   └── order.py
│   │
│   ├── routers/                   # Rotas da API
│   │   ├── auth.py                # /auth/*
│   │   ├── products.py            # /products/*
│   │   ├── cart.py                # /cart/*
│   │   ├── checkout.py            # /checkout
│   │   ├── payments.py            # /payments/*
│   │   └── orders.py              # /orders/*
│   │
│   └── tests/                     # Testes automatizados
│       ├── conftest.py
│       └── test_auth.py
│
├── data/                          # Banco de dados SQLite (gitignored)
│   └── ecommerce.db
│
├── .env                           # Variáveis de ambiente (gitignored)
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- pip
- (Opcional) Docker e Docker Compose

### 1️⃣ Clone o Repositório


### 2️⃣ Crie o Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

### 3️⃣ Instale as Dependências
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure as Variáveis de Ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
SECRET_KEY=sua-chave-secreta-super-segura-aqui-min-32-caracteres
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **⚠️ IMPORTANTE:** Gere uma chave secreta forte usando:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5️⃣ Execute a Aplicação
```bash
uvicorn app.main:app --reload
```

A API estará disponível em: `http://localhost:8000`

### 6️⃣ Acesse a Documentação Interativa
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 📚 Documentação da API

### Endpoints de Autenticação

#### `POST /auth/register`
Registra um novo usuário no sistema.

**Request:**
```json
{
  "email": "usuario@example.com",
  "password": "senhaSegura123"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "usuario@example.com",
  "is_admin": false
}
```

**Rate Limit:** 3 requisições/hora

---

#### `POST /auth/login`
Autentica um usuário e retorna um token JWT.

**Request (Form Data):**
```
username: usuario@example.com
password: senhaSegura123
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Rate Limit:** 5 requisições/minuto

---

### Endpoints de Produtos

#### `GET /products/`
Lista todos os produtos disponíveis (rota pública).

**Query Parameters:**
- `skip` (opcional): Número de registros para pular (padrão: 0)
- `limit` (opcional): Número máximo de resultados (padrão: 100)

**Response (200):**
```json
[
  {
    "id": 1,
    "name": "Notebook Dell",
    "description": "Intel i7, 16GB RAM, 512GB SSD",
    "price": 3500.00,
    "stock": 10
  }
]
```

---

#### `POST /products/` 🔒 Admin
Cria um novo produto (apenas administradores).

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "name": "Mouse Gamer",
  "description": "RGB, 16000 DPI",
  "price": 250.00,
  "stock": 50
}
```

**Response (201):**
```json
{
  "id": 2,
  "name": "Mouse Gamer",
  "description": "RGB, 16000 DPI",
  "price": 250.00,
  "stock": 50
}
```

---

#### `PATCH /products/{product_id}` 🔒 Admin
Atualiza um produto existente.

**Request:**
```json
{
  "price": 230.00,
  "stock": 45
}
```

---

#### `DELETE /products/{product_id}` 🔒 Admin
Remove um produto do catálogo.

**Response (204):** No Content

---

### Endpoints do Carrinho

#### `POST /cart/add` 🔒 User
Adiciona um produto ao carrinho do usuário.

**Headers:**
```
Authorization: Bearer {token}
```

**Request:**
```json
{
  "product_id": 1,
  "quantity": 2
}
```

**Response (200):**
```json
{
  "message": "Produto Notebook Dell adicionado ao carrinho"
}
```

**Validações:**
- Verifica se o produto existe
- Valida disponibilidade de estoque
- Atualiza quantidade se o produto já estiver no carrinho

---

### Endpoints de Checkout

#### `POST /checkout/` 🔒 User
Finaliza o carrinho e prepara para pagamento.

**Response (200):**
```json
{
  "message": "Checkout realizado com sucesso! Aguardando pagamento.",
  "order_id": 5,
  "total": 7000.00,
  "status": "pending_payment"
}
```

**Validações:**
- Verifica se o carrinho possui itens
- Re-valida estoque de todos os produtos
- Altera status do pedido para `PENDING_PAYMENT`

---

### Endpoints de Pagamento

#### `POST /payments/{order_id}` 🔒 User
Processa o pagamento de um pedido pendente.

**Response (200):**
```json
{
  "message": "Pagamento confirmado com sucesso!",
  "order_id": 5,
  "payment_reference": "a7f3c912-4b2e-4d89-9f1a-8c3d5e6f7a8b",
  "new_status": "paid"
}
```

**Ações Executadas:**
- Valida existência do pedido
- Re-valida estoque (safety check)
- **Baixa o estoque dos produtos**
- Altera status para `PAID`
- Gera referência UUID do pagamento

---

### Endpoints de Pedidos

#### `GET /orders/me` 🔒 User
Lista todos os pedidos do usuário autenticado.

**Response (200):**
```json
[
  {
    "id": 5,
    "status": "paid",
    "total": 7000.00,
    "created_at": "2024-01-19T10:30:00",
    "items": [
      {
        "product_id": 1,
        "quantity": 2,
        "unit_price": 3500.00
      }
    ]
  }
]
```

---

#### `GET /orders/{order_id}` 🔒 User
Detalha um pedido específico do usuário.

**Response (200):**
```json
{
  "id": 5,
  "status": "paid",
  "total": 7000.00,
  "created_at": "2024-01-19T10:30:00",
  "items": [
    {
      "product_id": 1,
      "quantity": 2,
      "unit_price": 3500.00
    }
  ]
}
```

---

#### `GET /orders/admin/all` 🔒 Admin
Lista todos os pedidos de todos os usuários (painel administrativo).

---

## 🔐 Autenticação

### Fluxo de Autenticação

1. **Registro**: Usuário cria conta via `/auth/register`
2. **Login**: Recebe token JWT via `/auth/login`
3. **Uso do Token**: Inclui token no header de requisições protegidas:
   ```
   Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   ```

### Exemplo com cURL
```bash
# 1. Fazer login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@example.com&password=senhaSegura123"

# Resposta: {"access_token": "TOKEN_AQUI", "token_type": "bearer"}

# 2. Usar token para adicionar ao carrinho
curl -X POST http://localhost:8000/cart/add \
  -H "Authorization: Bearer TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'
```

### Exemplo com Python Requests
```python
import requests

# Login
response = requests.post(
    "http://localhost:8000/auth/login",
    data={
        "username": "usuario@example.com",
        "password": "senhaSegura123"
    }
)
token = response.json()["access_token"]

# Usar token
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(
    "http://localhost:8000/cart/add",
    json={"product_id": 1, "quantity": 2},
    headers=headers
)
print(response.json())
```

---

## 🎯 Fluxo de Uso

### Cenário: Compra Completa de um Produto

```bash
# 1. Registrar usuário
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "cliente@email.com", "password": "senha123"}'

# 2. Fazer login
curl -X POST http://localhost:8000/auth/login \
  -d "username=cliente@email.com&password=senha123"

# Guardar o token retornado: export TOKEN="seu_token_aqui"

# 3. Listar produtos
curl http://localhost:8000/products/

# 4. Adicionar ao carrinho
curl -X POST http://localhost:8000/cart/add \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# 5. Finalizar checkout
curl -X POST http://localhost:8000/checkout/ \
  -H "Authorization: Bearer $TOKEN"

# Guardar o order_id retornado: export ORDER_ID=5

# 6. Processar pagamento
curl -X POST http://localhost:8000/payments/$ORDER_ID \
  -H "Authorization: Bearer $TOKEN"

# 7. Consultar histórico
curl http://localhost:8000/orders/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 🧪 Testes

### Executar Testes
```bash
pytest
```

### Executar com Cobertura
```bash
pytest --cov=app --cov-report=html
```

### Estrutura de Testes
```python
# app/tests/test_auth.py
def test_register_user(client):
    """Testa registro de novo usuário"""
    response = client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user(client):
    """Testa login de usuário existente"""
    # Primeiro registra
    client.post(
        "/auth/register",
        json={"email": "login@example.com", "password": "password123"}
    )
    # Depois tenta login
    response = client.post(
        "/auth/login",
        data={"username": "login@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

---

## 🐳 Deploy com Docker

### Construir e Executar
```bash
# Build da imagem
docker-compose build

# Executar em background
docker-compose up -d

# Ver logs
docker-compose logs -f

# Parar containers
docker-compose down
```

### Configuração de Produção
Para ambiente de produção, modifique o `docker-compose.yml`:

```yaml
version: "3.9"

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/app/data
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    restart: unless-stopped
```

E crie um arquivo `.env.production`:
```env
SECRET_KEY=chave-super-segura-de-producao
```

Execute com:
```bash
docker-compose --env-file .env.production up -d
```

---

## 🔒 Segurança

### Medidas Implementadas

#### 1. Autenticação JWT
- Tokens assinados com HS256
- Expiração configurável (padrão: 30 minutos)
- Validação de assinatura em cada requisição

#### 2. Criptografia de Senhas
- Hashing com Bcrypt (custo 12)
- Senhas nunca armazenadas em texto plano
- Verificação segura com `passlib`

#### 3. Rate Limiting
- **Registro:** 3 requisições/hora (previne spam)
- **Login:** 5 requisições/minuto (previne força bruta)
- **Global:** 200 requisições/dia, 50/hora

#### 4. Validação de Dados
- Pydantic valida todos os inputs
- Proteção contra SQL Injection (ORM)
- Validação de tipos e formatos (EmailStr, etc)

#### 5. Controle de Permissões
- Rotas protegidas por autenticação
- Separação de permissões (User vs Admin)
- Middleware de validação de token

### Boas Práticas Recomendadas

```bash
# ✅ Use HTTPS em produção
# ✅ Mantenha SECRET_KEY em variável de ambiente
# ✅ Use banco de dados PostgreSQL em produção
# ✅ Implemente logs de auditoria
# ✅ Configure CORS adequadamente
# ✅ Use rate limiting mais rigoroso em produção
# ✅ Implemente refresh tokens
# ✅ Adicione verificação de e-mail (2FA)
```

### Configurar CORS
Adicione em `app/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://seu-frontend.com"],  # Em produção, especifique domínios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---


## 🤝 Contribuindo

Contribuições são bem-vindas! Siga estes passos:

### 1. Fork o Projeto
```bash
git clone https://github.com/seu-usuario/ecommerce-api.git
cd ecommerce-api
```

### 2. Crie uma Branch
```bash
git checkout -b feature/nova-funcionalidade
```

### 3. Faça suas Alterações
```bash
# Adicione testes para novas funcionalidades
# Mantenha o código formatado (black, isort)
```

### 4. Commit suas Mudanças
```bash
git commit -m "feat: adiciona sistema de cupons de desconto"
```

### 5. Push para o GitHub
```bash
git push origin feature/nova-funcionalidade
```

### 6. Abra um Pull Request
Descreva suas mudanças e aguarde review!

### Padrões de Código
```bash
# Formatar código
black app/

# Ordenar imports
isort app/

# Linting
flake8 app/

# Type checking
mypy app/
```

---


## 🙏 Agradecimentos

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web incrível
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM poderoso
- [Pydantic](https://docs.pydantic.dev/) - Validação de dados
- Comunidade Python Brasil


---

**⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!**

