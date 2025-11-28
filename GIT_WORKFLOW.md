# Guia de Trabalho com Git - ConvençãoColetiva

## 🚀 Primeira Configuração (Já Feita)

O repositório já está configurado e conectado ao GitHub:
- **Repositório**: `https://github.com/AlexandreTessaro/convencao_coletiva.git`
- **Branch principal**: `main`

## 📝 Fluxo de Trabalho Diário

### 1. Verificar Status

Antes de fazer qualquer alteração, verifique o status:

```powershell
git status
```

### 2. Adicionar Mudanças

Depois de fazer alterações nos arquivos:

```powershell
# Adicionar todos os arquivos modificados
git add .

# OU adicionar arquivos específicos
git add backend/app/services/mediador_api.py
git add frontend/app/dashboard/page.tsx
```

### 3. Fazer Commit

Sempre faça commits descritivos:

```powershell
# Commit simples
git commit -m "feat: adiciona busca em tempo real no Mediador MTE"

# Commit com descrição detalhada
git commit -m "feat: adiciona busca em tempo real no Mediador MTE

- Implementa busca direta no site Mediador MTE
- Adiciona filtros por CNAE, município e UF
- Melhora tratamento de encoding UTF-8"
```

### 4. Enviar para GitHub (Push)

```powershell
# Enviar para a branch main
git push origin main

# OU se já configurou upstream
git push
```

## 📋 Convenções de Commit

Use mensagens descritivas seguindo o padrão:

- `feat:` - Nova funcionalidade
- `fix:` - Correção de bug
- `docs:` - Documentação
- `style:` - Formatação (não afeta código)
- `refactor:` - Refatoração
- `test:` - Testes
- `chore:` - Tarefas de manutenção

**Exemplos:**
```powershell
git commit -m "feat: adiciona sistema de alertas de dissídio"
git commit -m "fix: corrige encoding UTF-8 nos resultados da busca"
git commit -m "docs: atualiza README com instruções de instalação"
git commit -m "refactor: reorganiza estrutura de pastas do backend"
```

## 🔄 Fluxo Completo de Trabalho

### Cenário 1: Trabalhando em uma nova funcionalidade

```powershell
# 1. Verificar status atual
git status

# 2. Criar uma nova branch (opcional, mas recomendado)
git checkout -b feature/nova-funcionalidade

# 3. Fazer suas alterações nos arquivos...

# 4. Adicionar mudanças
git add .

# 5. Fazer commit
git commit -m "feat: descrição da funcionalidade"

# 6. Enviar para GitHub
git push origin feature/nova-funcionalidade

# 7. Depois, fazer merge na main (via GitHub ou localmente)
git checkout main
git merge feature/nova-funcionalidade
git push origin main
```

### Cenário 2: Trabalhando diretamente na main (para mudanças pequenas)

```powershell
# 1. Verificar status
git status

# 2. Fazer alterações...

# 3. Adicionar e commitar
git add .
git commit -m "fix: corrige bug específico"

# 4. Enviar para GitHub
git push origin main
```

## 🔍 Comandos Úteis

### Ver histórico de commits
```powershell
git log --oneline
git log --graph --oneline --all
```

### Ver diferenças antes de commitar
```powershell
# Ver mudanças não commitadas
git diff

# Ver mudanças já adicionadas ao staging
git diff --staged
```

### Desfazer mudanças

```powershell
# Desfazer mudanças em arquivo não commitado
git restore arquivo.py

# Remover arquivo do staging (mas manter mudanças)
git restore --staged arquivo.py

# Desfazer último commit (mantendo mudanças)
git reset --soft HEAD~1

# Desfazer último commit (perdendo mudanças)
git reset --hard HEAD~1
```

### Atualizar do GitHub

```powershell
# Baixar mudanças do GitHub
git pull origin main

# OU
git fetch origin
git merge origin/main
```

## ⚠️ Boas Práticas

1. **Sempre faça `git status` antes de commitar** - Verifique o que será commitado
2. **Commits frequentes** - Faça commits pequenos e frequentes, não um commit gigante
3. **Mensagens descritivas** - Use mensagens claras sobre o que foi alterado
4. **Não commite arquivos sensíveis** - `.env`, senhas, tokens, etc. devem estar no `.gitignore`
5. **Teste antes de fazer push** - Certifique-se de que o código funciona antes de enviar
6. **Faça pull antes de push** - Se trabalhar em múltiplos computadores, sempre faça pull primeiro

## 🐛 Resolução de Problemas

### Erro: "Your branch is ahead of 'origin/main'"
```powershell
# Significa que você tem commits locais que não foram enviados
git push origin main
```

### Erro: "Your branch is behind 'origin/main'"
```powershell
# Significa que há commits no GitHub que você não tem localmente
git pull origin main
```

### Conflitos de merge
```powershell
# Se houver conflitos ao fazer pull
git pull origin main
# Resolver conflitos manualmente nos arquivos
# Depois:
git add .
git commit -m "fix: resolve conflitos de merge"
git push origin main
```

### Desfazer último push (CUIDADO!)
```powershell
# Se precisar desfazer um commit já enviado
git revert HEAD
git push origin main
```

## 📚 Recursos Adicionais

- [Documentação oficial do Git](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## 🎯 Checklist Antes de Fazer Push

- [ ] Código testado e funcionando
- [ ] Arquivos sensíveis não estão sendo commitados (`.env`, etc.)
- [ ] Mensagem de commit descritiva
- [ ] `git status` mostra apenas arquivos relevantes
- [ ] Não há arquivos de build ou temporários (`node_modules`, `__pycache__`, etc.)

