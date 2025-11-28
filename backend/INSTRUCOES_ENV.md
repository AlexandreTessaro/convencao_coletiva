# Configuração do arquivo .env

## Criar arquivo .env

Execute o script PowerShell:

```powershell
cd backend
.\create_env.ps1
```

Ou crie manualmente o arquivo `backend/.env` com o seguinte conteúdo:

```env
# Database
# IMPORTANTE: Substitua SUA_SENHA_POSTGRES_AQUI pela senha real do PostgreSQL
DATABASE_URL=postgresql://postgres:SUA_SENHA_POSTGRES_AQUI@localhost:5432/convencao_coletiva

# Security
# IMPORTANTE: Gere uma SECRET_KEY segura com: openssl rand -hex 32
# OU use o script create_env.ps1 que gera automaticamente
SECRET_KEY=GERE_UMA_SECRET_KEY_SEGURA_AQUI
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
# IMPORTANTE: Configure suas credenciais SMTP reais abaixo
# Exemplo de configuração (SUBSTITUA pelos valores reais):
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=SUBSTITUA_PELO_SEU_EMAIL_AQUI
SMTP_PASSWORD=SUBSTITUA_PELA_SUA_SENHA_SMTP_AQUI
SMTP_FROM=noreply@convencaocoletiva.com.br

# Storage
STORAGE_TYPE=local
STORAGE_PATH=./storage

# Scraper
SCRAPER_DELAY_SECONDS=3
SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
MEDIADOR_BASE_URL=https://mediador.trabalho.gov.br

# OCR
TESSERACT_CMD=/usr/bin/tesseract
OCR_LANG=por
```

## Próximos passos após criar o .env

1. **Certifique-se de que o PostgreSQL está rodando**
   ```powershell
   # Verificar se PostgreSQL está rodando na porta 5432
   ```

2. **Crie o banco de dados** (se ainda não existir):
   ```sql
   CREATE DATABASE convencao_coletiva;
   ```

3. **Execute as migrações**:
   ```powershell
   cd backend
   .\venv\Scripts\Activate.ps1
   alembic upgrade head
   ```

4. **Inicie o servidor**:
   ```powershell
   python run.py
   ```

O servidor estará disponível em: http://localhost:8000

Documentação da API: http://localhost:8000/api/docs

