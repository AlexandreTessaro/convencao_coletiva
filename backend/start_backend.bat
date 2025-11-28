@echo off
echo Iniciando backend ConvencaoColetiva...

REM Verificar se .env existe
if not exist .env (
    echo Arquivo .env nao encontrado. Criando a partir do exemplo...
    if exist .env.example (
        copy .env.example .env
        echo Arquivo .env criado. Por favor, configure as variaveis de ambiente.
        pause
    ) else (
        echo ERRO: Arquivo .env.example nao encontrado!
        pause
        exit /b 1
    )
)

REM Verificar se venv existe
if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

REM Ativar ambiente virtual
call venv\Scripts\activate.bat

REM Instalar dependências
echo Verificando dependencias...
pip install -q -r requirements.txt

REM Iniciar servidor
echo Iniciando servidor backend na porta 8000...
echo Acesse a documentacao em: http://localhost:8000/api/docs
echo Pressione Ctrl+C para parar o servidor
echo.

python run.py

