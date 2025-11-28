# Script para executar migracoes
Write-Host "Executando migracoes do banco de dados..." -ForegroundColor Green

# Verificar se venv existe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    exit 1
}

# Ativar venv
& ".\venv\Scripts\Activate.ps1"

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "AVISO: Arquivo .env nao encontrado!" -ForegroundColor Yellow
    Write-Host "Execute: .\create_env_simple.ps1" -ForegroundColor Yellow
    exit 1
}

# Criar migracao inicial se nao existir
$migrationExists = Test-Path "alembic\versions\*.py"
if (-not $migrationExists) {
    Write-Host "Criando migracao inicial..." -ForegroundColor Cyan
    & ".\venv\Scripts\python.exe" -m alembic revision --autogenerate -m "Initial migration"
}

# Executar migracoes
Write-Host "Aplicando migracoes..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" -m alembic upgrade head

Write-Host "Migracoes executadas com sucesso!" -ForegroundColor Green

