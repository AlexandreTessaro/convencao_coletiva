# Script PowerShell para executar coleta de convenções
# Uso: .\collect_convencoes.ps1 [limit]
# Exemplo: .\collect_convencoes.ps1 10

param(
    [int]$Limit = 0
)

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "Coleta de Convenções do Mediador MTE" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Ativar ambiente virtual
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Ativando ambiente virtual..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
} else {
    Write-Host "⚠️  Ambiente virtual não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: python -m venv venv" -ForegroundColor Yellow
    exit 1
}

# Verificar se .env existe
if (-not (Test-Path ".\.env")) {
    Write-Host "⚠️  Arquivo .env não encontrado!" -ForegroundColor Red
    Write-Host "Execute primeiro: .\create_env.ps1" -ForegroundColor Yellow
    exit 1
}

# Executar coleta
Write-Host "Iniciando coleta..." -ForegroundColor Green
Write-Host ""
Write-Host "Dica: Se nenhuma convenção for encontrada, use:" -ForegroundColor Yellow
Write-Host "  python collect_with_fallback.py $Limit" -ForegroundColor Yellow
Write-Host "  (Isso criará dados de exemplo automaticamente)" -ForegroundColor Yellow
Write-Host ""

if ($Limit -gt 0) {
    python collect_convencoes.py $Limit
} else {
    python collect_convencoes.py
}

$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host ""
    Write-Host "✅ Coleta concluída com sucesso!" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Erro na coleta. Verifique os logs acima." -ForegroundColor Red
}

exit $exitCode

