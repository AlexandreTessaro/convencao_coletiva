# Script para iniciar o servidor backend
Write-Host "Iniciando servidor backend..." -ForegroundColor Green

# Verificar se venv existe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    Write-Host "Execute: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Ativar venv
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Verificar se uvicorn esta instalado
$uvicornInstalled = & ".\venv\Scripts\python.exe" -m pip list | Select-String "uvicorn"
if (-not $uvicornInstalled) {
    Write-Host "Instalando dependencias..." -ForegroundColor Yellow
    & ".\venv\Scripts\python.exe" -m pip install -r requirements.txt
}image.png

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "AVISO: Arquivo .env nao encontrado!" -ForegroundColor Yellow
    Write-Host "Execute: .\create_env_simple.ps1" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Iniciando servidor na porta 8000..." -ForegroundColor Green
Write-Host "Acesse: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para parar" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
& ".\venv\Scripts\python.exe" run.py

