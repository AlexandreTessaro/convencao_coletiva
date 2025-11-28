# Como Reiniciar o Servidor Backend

## ⚠️ IMPORTANTE: O servidor DEVE ser reiniciado após mudanças no código!

## Passos para Reiniciar:

### 1. Pare o servidor atual
No terminal onde o servidor está rodando:
- Pressione `Ctrl+C` para parar o servidor

### 2. Reinicie o servidor

**Opção A: Usando o script**
```powershell
cd backend
.\restart_server.ps1
```

**Opção B: Manualmente**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
python run.py
```

## Verificação

Após reiniciar, você deve ver:
- `INFO:     Uvicorn running on http://127.0.0.1:8000`
- `INFO:     Application startup complete.`

## Teste

1. Acesse: http://localhost:8000/api/docs
2. Tente criar uma conta no frontend novamente

## Se ainda houver erro

Verifique os logs do servidor no terminal. Eles mostrarão:
- Se a senha foi truncada
- Qualquer erro detalhado



