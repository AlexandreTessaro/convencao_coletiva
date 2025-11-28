# Guia de Setup - ConvençãoColetiva MVP

## 📋 Pré-requisitos

- Python 3.9+
- Node.js 18+
- PostgreSQL 14+
- Redis (para Celery)
- Tesseract OCR (para processamento de PDFs escaneados)
- Docker e Docker Compose (opcional, mas recomendado)

## 🚀 Setup Rápido com Docker

### 1. Iniciar serviços (PostgreSQL e Redis)

```bash
docker-compose up -d
```

### 2. Backend

```bash
cd backend

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Executar migrações
alembic upgrade head

# Iniciar servidor
python run.py
```

### 3. Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com a URL da API (http://localhost:8000)

# Iniciar servidor de desenvolvimento
npm run dev
```

### 4. Celery Worker (para coleta automática)

```bash
cd backend
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Iniciar worker
celery -A app.tasks.collector.celery_app worker --loglevel=info
```

## 🔧 Configuração Detalhada

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@localhost:5432/convencao_coletiva
SECRET_KEY=sua-chave-secreta-aqui
CORS_ORIGINS=http://localhost:3000
REDIS_URL=redis://localhost:6379/0
```

### Frontend (.env)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📝 Primeiros Passos

1. **Criar conta:**
   - Acesse `http://localhost:3000/register`
   - Crie uma conta de usuário

2. **Cadastrar empresa:**
   - Após login, vá para "Empresas"
   - Clique em "Adicionar Empresa"
   - Preencha CNPJ, CNAE, município, etc.

3. **Coletar convenções:**
   - Execute manualmente a tarefa de coleta (via API ou Celery)
   - Ou aguarde a execução automática agendada

## 🧪 Testar API

Acesse a documentação interativa em:
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

## 📚 Documentação

Consulte a pasta `docs/` para documentação completa:
- Arquitetura
- Fluxo de coleta
- Backlog
- Prototipação

## ⚠️ Notas Importantes

1. **Tesseract OCR:** Necessário para processar PDFs escaneados
   - Linux: `sudo apt-get install tesseract-ocr tesseract-ocr-por`
   - Mac: `brew install tesseract tesseract-lang`
   - Windows: Baixar de https://github.com/UB-Mannheim/tesseract/wiki

2. **ChromeDriver:** Necessário para o scraper Selenium
   - Instalar Chrome e ChromeDriver
   - Ou usar Selenium Grid

3. **Mediador MTE:** 
   - Validar termos de uso antes de usar em produção
   - Ajustar seletores CSS no scraper conforme estrutura do site

## 🐛 Troubleshooting

### Erro de conexão com banco
- Verifique se PostgreSQL está rodando
- Confirme credenciais no .env

### Erro de CORS
- Adicione a URL do frontend em CORS_ORIGINS no .env do backend

### Erro no scraper
- Verifique se Chrome/ChromeDriver está instalado
- Ajuste seletores CSS conforme estrutura do site Mediador MTE

## 📞 Suporte

Para dúvidas, consulte a documentação em `docs/` ou abra uma issue no repositório.

