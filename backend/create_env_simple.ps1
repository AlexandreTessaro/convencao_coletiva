# Script simples para criar arquivo .env
# Gera uma SECRET_KEY aleatória segura
$secretKey = -join ((48..57) + (65..90) + (97..122) | Get-Random -Count 64 | ForEach-Object {[char]$_})

$lines = @(
    "# Database",
    "DATABASE_URL=postgresql://postgres:SUA_SENHA_POSTGRES_AQUI@localhost:5432/convencao_coletiva",
    "",
    "# Security",
    "# SECRET_KEY gerada automaticamente - altere se necessário",
    "SECRET_KEY=$secretKey",
    "ALGORITHM=HS256",
    "ACCESS_TOKEN_EXPIRE_MINUTES=30",
    "",
    "# CORS",
    "CORS_ORIGINS=http://localhost:3000,http://localhost:3001",
    "",
    "# Redis (for Celery)",
    "REDIS_URL=redis://localhost:6379/0",
    "",
    "# Email (for notifications)",
    "# Configure suas credenciais SMTP reais abaixo",
    "SMTP_HOST=smtp.gmail.com",
    "SMTP_PORT=587",
    "SMTP_USER=seu-email@gmail.com",
    "SMTP_PASSWORD=SUA_SENHA_SMTP_AQUI",
    "SMTP_FROM=noreply@convencaocoletiva.com.br",
    "",
    "# Storage",
    "STORAGE_TYPE=local",
    "STORAGE_PATH=./storage",
    "",
    "# Scraper",
    "SCRAPER_DELAY_SECONDS=3",
    "SCRAPER_USER_AGENT=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "MEDIADOR_BASE_URL=https://mediador.trabalho.gov.br",
    "",
    "# OCR",
    "TESSERACT_CMD=/usr/bin/tesseract",
    "OCR_LANG=por"
)

$lines | Out-File -FilePath ".env" -Encoding utf8

Write-Host "Arquivo .env criado com sucesso!" -ForegroundColor Green

