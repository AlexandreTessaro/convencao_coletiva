# Solução para Problemas de CORS e Erro 500

## Problema Identificado

1. **CORS**: O servidor não está permitindo requisições do frontend
2. **Erro 500**: Tabelas do banco de dados não existem (migrações não executadas)

## Solução

### 1. Execute as Migrações (CRÍTICO)

No terminal PowerShell, no diretório `backend`:

```powershell
.\venv\Scripts\Activate.ps1
alembic upgrade head
```

Ou use o script:
```powershell
.\run_migrations.ps1
```

Isso criará todas as tabelas necessárias no banco de dados.

### 2. Reinicie o Servidor Backend

**IMPORTANTE**: O servidor precisa ser reiniciado para aplicar as mudanças de CORS.

```powershell
# Pare o servidor atual (Ctrl+C se estiver rodando)

# Reinicie
.\venv\Scripts\Activate.ps1
python run.py
```

Ou use o script:
```powershell
.\restart_server.ps1
```

### 3. Verifique se Está Funcionando

1. **Backend**: http://localhost:8000/api/docs
2. **Health Check**: http://localhost:8000/health
3. **Frontend**: http://localhost:3000

## Configuração de CORS Aplicada

O CORS está configurado para permitir:
- `http://localhost:3000`
- `http://localhost:3001`
- `http://127.0.0.1:3000`
- `http://127.0.0.1:3001`

## Se Ainda Houver Erro

1. Verifique os logs do servidor backend no terminal
2. Verifique se o PostgreSQL está rodando
3. Verifique se o banco de dados `convencao_coletiva` existe
4. Verifique se as migrações foram executadas com sucesso

## Comandos Úteis

```powershell
# Verificar status das migrações
.\venv\Scripts\Activate.ps1
alembic current

# Ver histórico de migrações
alembic history

# Criar nova migração (se necessário)
alembic revision --autogenerate -m "descrição"

# Reverter última migração (cuidado!)
alembic downgrade -1
```

