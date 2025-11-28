# Script para criar dados de teste
Write-Host "Criando dados de teste..." -ForegroundColor Green

# Verificar se venv existe
if (-not (Test-Path "venv\Scripts\python.exe")) {
    Write-Host "ERRO: Ambiente virtual nao encontrado!" -ForegroundColor Red
    exit 1
}

# Ativar venv
& ".\venv\Scripts\Activate.ps1"

# Executar script Python
Write-Host "Executando script de criacao de dados de teste..." -ForegroundColor Cyan
& ".\venv\Scripts\python.exe" create_test_data.py

Write-Host ""
Write-Host "Dados de teste criados!" -ForegroundColor Green



