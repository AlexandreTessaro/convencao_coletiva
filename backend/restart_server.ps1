# Script para reiniciar o servidor backend
Write-Host "Reiniciando servidor backend..." -ForegroundColor Green

# Verificar se venv existe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    exit 1
}

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "AVISO: Arquivo .env nao encontrado!" -ForegroundColor Yellow
    Write-Host "Execute: .\create_env_simple.ps1" -ForegroundColor Yellow
    exit 1
}

# Verificar se migracoes foram executadas
Write-Host "Verificando migracoes..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" -m alembic current

Write-Host ""
Write-Host "Iniciando servidor na porta 8000..." -ForegroundColor Green
Write-Host "Acesse: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
& ".\venv\Scripts\python.exe" run.py

