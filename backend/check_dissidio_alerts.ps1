# Script PowerShell para executar verificação de alertas de dissídio
Write-Host "Verificando alertas de dissídio..." -ForegroundColor Cyan

# Ativar ambiente virtual se existir
if (Test-Path .\venv\Scripts\Activate.ps1) {
    .\venv\Scripts\Activate.ps1
    Write-Host "Ambiente virtual ativado" -ForegroundColor Green
}

# Executar script Python
python check_dissidio_alerts.py

# Pausar para ver resultado
Write-Host "`nPressione qualquer tecla para continuar..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

