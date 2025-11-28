# Backend - ConvençãoColetiva API

## 🚀 Setup

### Pré-requisitos

- Python 3.9+
- PostgreSQL 14+
- Redis (para Celery)
- Tesseract OCR (para processamento de PDFs escaneados)

### Instalação

1. **Criar ambiente virtual:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

2. **Instalar dependências:**
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente:**
```bash
cp .env.example .env
# Editar .env com suas configurações
```

4. **Configurar banco de dados:**
```bash
# Criar banco de dados PostgreSQL
createdb convencao_coletiva

# Executar migrações
alembic upgrade head
```

5. **Instalar Tesseract OCR:**
- **Linux:** `sudo apt-get install tesseract-ocr tesseract-ocr-por`
- **Mac:** `brew install tesseract tesseract-lang`
- **Windows:** Baixar de https://github.com/UB-Mannheim/tesseract/wiki

### Executar

```bash
# Desenvolvimento
python run.py

# Ou com uvicorn diretamente
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

A API estará disponível em `http://localhost:8000`

Documentação interativa: `http://localhost:8000/api/docs`

## 📋 Estrutura

```
backend/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── endpoints/     # Rotas da API
│   │       └── api.py         # Router principal
│   ├── core/
│   │   ├── config.py          # Configurações
│   │   ├── database.py        # Conexão com banco
│   │   └── security.py        # Autenticação/JWT
│   ├── models/                # Modelos SQLAlchemy
│   ├── schemas/               # Schemas Pydantic
│   ├── services/              # Serviços (scraper, processador)
│   └── tasks/                 # Tarefas Celery
├── alembic/                   # Migrações do banco
├── requirements.txt
└── run.py
```

## 🔧 Comandos Úteis

### Migrações

```bash
# Criar nova migração
alembic revision --autogenerate -m "descrição"

# Aplicar migrações
alembic upgrade head

# Reverter migração
alembic downgrade -1
```

### Celery (Coleta Automática)

```bash
# Iniciar worker
celery -A app.tasks.collector.celery_app worker --loglevel=info

# Agendar tarefa (em Python)
from app.tasks.collector import collect_convencoes_task
collect_convencoes_task.delay()
```

## 📚 Endpoints Principais

- `POST /api/v1/auth/register` - Cadastro de usuário
- `POST /api/v1/auth/login` - Login
- `GET /api/v1/auth/me` - Informações do usuário atual
- `GET /api/v1/companies` - Listar empresas
- `POST /api/v1/companies` - Cadastrar empresa
- `GET /api/v1/convencoes/search` - Buscar convenções
- `GET /api/v1/notifications` - Listar notificações
- `GET /api/v1/dashboard/stats` - Estatísticas do dashboard

## 🔐 Autenticação

A API usa JWT (JSON Web Tokens). Após fazer login, inclua o token no header:

```
Authorization: Bearer <token>
```

## 🧪 Testes

```bash
# Instalar dependências de teste
pip install pytest pytest-cov

# Executar testes
pytest

# Com cobertura
pytest --cov=app
```

