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
DATABASE_URL=postgresql://postgres:gajseEwNF2KO0a2KfW1w@localhost:5432/convencao_coletiva

# Security
SECRET_KEY=a490394c74a005366dcac80215bc13b69e56724c32f4f98bba444210d6c84d4a
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
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

