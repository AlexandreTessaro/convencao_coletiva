# Script para criar arquivo .env com as credenciais do PostgreSQL
Write-Host "Criando arquivo .env..." -ForegroundColor Green

# Gera uma SECRET_KEY aleatória segura (64 caracteres hexadecimais)
$bytes = New-Object byte[] 32
[System.Security.Cryptography.RandomNumberGenerator]::Fill($bytes)
$secretKey = ($bytes | ForEach-Object { $_.ToString("x2") }) -join ""

Write-Host "Gerando SECRET_KEY segura..." -ForegroundColor Cyan

$envContent = @"
# Database
# IMPORTANTE: Substitua SUA_SENHA_POSTGRES_AQUI pela senha real do PostgreSQL
DATABASE_URL=postgresql://postgres:SUA_SENHA_POSTGRES_AQUI@localhost:5432/convencao_coletiva

# Security
# SECRET_KEY gerada automaticamente - mantenha segura e não compartilhe
SECRET_KEY=$secretKey
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Redis (for Celery)
REDIS_URL=redis://localhost:6379/0

# Email (for notifications)
# IMPORTANTE: Configure suas credenciais SMTP reais abaixo
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=seu-email@gmail.com
SMTP_PASSWORD=SUA_SENHA_SMTP_AQUI
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
Write-Host "  - Database: Configure SUA_SENHA_POSTGRES_AQUI no arquivo .env" -ForegroundColor Yellow
Write-Host "  - SECRET_KEY: Gerada automaticamente (mantenha segura!)" -ForegroundColor Yellow
Write-Host "  - SMTP: Configure SUA_SENHA_SMTP_AQUI no arquivo .env" -ForegroundColor Yellow
Write-Host ""
Write-Host "Proximos passos:" -ForegroundColor Cyan
Write-Host '  - Certifique-se de que o PostgreSQL esta rodando' -ForegroundColor White
Write-Host '  - Crie o banco de dados: CREATE DATABASE convencao_coletiva;' -ForegroundColor White
Write-Host '  - Execute as migracoes: alembic upgrade head' -ForegroundColor White
Write-Host '  - Inicie o servidor: python run.py' -ForegroundColor White

