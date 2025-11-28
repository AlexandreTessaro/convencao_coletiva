# Como Iniciar o Backend

O erro `ERR_CONNECTION_REFUSED` indica que o servidor backend não está rodando.

## Opção 1: Usar o Script Automático (Recomendado)

### Windows PowerShell:
```powershell
cd backend
.\start_backend.ps1
```

### Windows CMD:
```cmd
cd backend
start_backend.bat
```

## Opção 2: Manual

### 1. Navegar para o diretório backend:
```powershell
cd backend
```

### 2. Criar arquivo .env (se não existir):
```powershell
Copy-Item .env.example .env
```

**IMPORTANTE:** Edite o arquivo `.env` e configure pelo menos:
- `DATABASE_URL` - URL do PostgreSQL
- `SECRET_KEY` - Chave secreta (gere uma nova com: `openssl rand -hex 32`)

### 3. Criar ambiente virtual (se não existir):
```powershell
python -m venv venv
```

### 4. Ativar ambiente virtual:
```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Instalar dependências:
```powershell
pip install -r requirements.txt
```

### 6. Configurar banco de dados:
```powershell
# Certifique-se de que o PostgreSQL está rodando
# Execute as migrações:
alembic upgrade head
```

### 7. Iniciar servidor:
```powershell
python run.py
```

O servidor estará disponível em: `http://localhost:8000`

Documentação da API: `http://localhost:8000/api/docs`

## Verificar se está funcionando

Abra outro terminal e teste:
```powershell
curl http://localhost:8000/health
```

Ou acesse no navegador: http://localhost:8000/api/docs

## Troubleshooting

### Erro de conexão com banco de dados:
- Verifique se o PostgreSQL está rodando
- Confirme as credenciais no `.env`
- Teste a conexão: `psql -U user -d convencao_coletiva`

### Erro de porta já em uso:
- Altere a porta no `run.py` ou mate o processo que está usando a porta 8000

### Erro de módulo não encontrado:
- Certifique-se de que o ambiente virtual está ativado
- Execute `pip install -r requirements.txt` novamente

