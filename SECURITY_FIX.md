# 🔒 Correção de Segurança - Credenciais Expostas

## ⚠️ Problema Identificado

O GitGuardian detectou credenciais expostas no repositório:
- **SECRET_KEY** hardcoded em scripts
- **Senha do PostgreSQL** hardcoded em scripts
- **Credenciais SMTP** de exemplo em documentação

## ✅ Correções Aplicadas

### 1. Scripts Atualizados

**`backend/create_env.ps1`** e **`backend/create_env_simple.ps1`**:
- ✅ Removida SECRET_KEY hardcoded
- ✅ Scripts agora geram SECRET_KEY aleatória automaticamente
- ✅ Removida senha do PostgreSQL hardcoded
- ✅ Substituída por placeholder `SUA_SENHA_POSTGRES_AQUI`
- ✅ Credenciais SMTP substituídas por placeholders

### 2. Documentação Atualizada

**`backend/INSTRUCOES_ENV.md`**:
- ✅ Removidas todas as credenciais hardcoded
- ✅ Adicionadas instruções para gerar SECRET_KEY segura
- ✅ Placeholders claros para todas as credenciais

### 3. Arquivo .env.example Criado

**`backend/.env.example`**:
- ✅ Template seguro sem credenciais reais
- ✅ Instruções claras para cada variável

## 🔐 Ações Necessárias

### ⚠️ IMPORTANTE: Regenerar Credenciais Comprometidas

Como a SECRET_KEY foi exposta no histórico do Git, você **DEVE**:

1. **Regenerar a SECRET_KEY** no seu ambiente de produção:
   ```powershell
   # Gerar nova SECRET_KEY
   openssl rand -hex 32
   ```
   
   OU use o script atualizado que gera automaticamente:
   ```powershell
   cd backend
   .\create_env.ps1
   ```

2. **Alterar a senha do PostgreSQL** se ela foi comprometida:
   ```sql
   ALTER USER postgres WITH PASSWORD 'NOVA_SENHA_SEGURA';
   ```

3. **Rotacionar tokens JWT** (usuários precisarão fazer login novamente):
   - A SECRET_KEY antiga não funcionará mais
   - Todos os tokens JWT existentes serão invalidados
   - Usuários precisarão fazer login novamente

### 📝 Como Usar os Scripts Atualizados

```powershell
cd backend

# O script agora gera SECRET_KEY automaticamente
.\create_env.ps1

# Depois, edite o arquivo .env gerado e configure:
# - SUA_SENHA_POSTGRES_AQUI → senha real do PostgreSQL
# - SUA_SENHA_SMTP_AQUI → senha real do SMTP (se usar)
```

## 🛡️ Prevenção Futura

### ✅ Boas Práticas Implementadas

1. ✅ `.env` está no `.gitignore` (não será commitado)
2. ✅ Scripts geram credenciais dinamicamente
3. ✅ Documentação usa apenas placeholders
4. ✅ `.env.example` criado como template seguro

### 📋 Checklist Antes de Commitar

Sempre verifique antes de fazer commit:

```powershell
# Verificar se há credenciais hardcoded
git diff | Select-String -Pattern "password|secret|key|token" -CaseSensitive:$false

# Verificar se arquivo .env não está sendo commitado
git status | Select-String "\.env"

# Ver o que será commitado
git status
```

### 🔍 Comandos Úteis

```powershell
# Buscar por possíveis credenciais no código
git grep -i "password\|secret\|key\|token" -- "*.ps1" "*.md" "*.py"

# Ver histórico de commits (para verificar se há mais credenciais)
git log --all --full-history --source -- "*.env" "*.ps1"
```

## 📚 Recursos

- [GitGuardian - Remediate Secret Leaks](https://docs.gitguardian.com/remediating-secrets/)
- [OWASP - Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub - Removing sensitive data](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository)

## ⚠️ Nota Importante

**O histórico do Git ainda contém as credenciais antigas**. Se você precisa remover completamente do histórico:

1. Considere usar `git filter-branch` ou `git filter-repo` (mais seguro)
2. **CUIDADO**: Isso reescreve o histórico e pode afetar colaboradores
3. **Recomendação**: Se o repositório é novo e não tem muitos commits, considere criar um novo repositório

Para um repositório novo como este, a melhor opção pode ser:
- As credenciais já foram removidas dos arquivos atuais
- O histórico ainda contém, mas como é um repositório novo, o risco é menor
- Foque em garantir que não há mais credenciais nos commits futuros

---

**Status**: ✅ Credenciais removidas dos arquivos atuais
**Próximo passo**: Regenerar SECRET_KEY no ambiente de produção

