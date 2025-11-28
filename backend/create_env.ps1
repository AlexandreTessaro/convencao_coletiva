# Script para criar arquivo .env com as credenciais do PostgreSQL
Write-Host "Criando arquivo .env..." -ForegroundColor Green

$secretKey = "a490394c74a005366dcac80215bc13b69e56724c32f4f98bba444210d6c84d4a"

$envContent = @"
# Database
DATABASE_URL=postgresql://postgres:gajseEwNF2KO0a2KfW1w@localhost:5432/convencao_coletiva

# Security
SECRET_KEY=$secretKey
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
"@

$envContent | Out-File -FilePath ".env" -Encoding utf8 -NoNewline

Write-Host "✓ Arquivo .env criado com sucesso!" -ForegroundColor Green
Write-Host ""
Write-Host "Configurações aplicadas:" -ForegroundColor Cyan
Write-Host "  - Database: postgresql://postgres:***@localhost:5432/convencao_coletiva" -ForegroundColor Yellow
Write-Host "  - SECRET_KEY: Configurado" -ForegroundColor Yellow
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host '  - Certifique-se de que o PostgreSQL esta rodando' -ForegroundColor White
Write-Host '  - Crie o banco de dados: CREATE DATABASE convencao_coletiva;' -ForegroundColor White
Write-Host '  - Execute as migracoes: alembic upgrade head' -ForegroundColor White
Write-Host '  - Inicie o servidor: python run.py' -ForegroundColor White

