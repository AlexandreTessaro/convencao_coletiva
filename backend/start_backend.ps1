# Script para iniciar o backend
Write-Host "Iniciando backend ConvençãoColetiva..." -ForegroundColor Green

# Verificar se .env existe
if (-not (Test-Path ".env")) {
    Write-Host "Arquivo .env não encontrado. Criando a partir do exemplo..." -ForegroundColor Yellow
    if (Test-Path ".env.example") {
        Copy-Item ".env.example" ".env"
        Write-Host "Arquivo .env criado. Por favor, configure as variáveis de ambiente antes de continuar." -ForegroundColor Yellow
        Write-Host "Pressione qualquer tecla após configurar o .env..."
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    } else {
        Write-Host "ERRO: Arquivo .env.example não encontrado!" -ForegroundColor Red
        exit 1
    }
}

# Verificar se venv existe
if (-not (Test-Path "venv")) {
    Write-Host "Criando ambiente virtual..." -ForegroundColor Yellow
    python -m venv venv
}

# Ativar ambiente virtual
Write-Host "Ativando ambiente virtual..." -ForegroundColor Cyan
& ".\venv\Scripts\Activate.ps1"

# Instalar dependências se necessário
Write-Host "Verificando dependências..." -ForegroundColor Cyan
pip install -q -r requirements.txt

# Verificar se banco de dados está configurado
Write-Host "Iniciando servidor backend na porta 8000..." -ForegroundColor Green
Write-Host "Acesse a documentação em: http://localhost:8000/api/docs" -ForegroundColor Cyan
Write-Host "Pressione Ctrl+C para parar o servidor" -ForegroundColor Yellow
Write-Host ""

# Iniciar servidor
python run.py

