# Backlog Inicial

## 📋 Épicos

### Épico 1: Autenticação e Gestão de Usuários
**Descrição:** Sistema de autenticação e gerenciamento de contas de usuários.

**Objetivo:** Permitir que usuários criem contas, façam login e gerenciem seus perfis.

---

### Épico 2: Gestão de Empresas
**Descrição:** Cadastro e gerenciamento de empresas para monitoramento.

**Objetivo:** Permitir que usuários cadastrem empresas e associem convenções.

---

### Épico 3: Coleta Automática de Dados
**Descrição:** Sistema automatizado para coletar convenções do Mediador MTE.

**Objetivo:** Coletar, processar e armazenar convenções automaticamente.

---

### Épico 4: Busca e Visualização
**Descrição:** Funcionalidades de busca e visualização de convenções.

**Objetivo:** Permitir que usuários encontrem e visualizem convenções facilmente.

---

### Épico 5: Notificações
**Descrição:** Sistema de notificações para novas convenções.

**Objetivo:** Alertar usuários sobre convenções relevantes.

---

### Épico 6: Dashboard
**Descrição:** Interface principal com visão geral e estatísticas.

**Objetivo:** Fornecer visão consolidada do sistema para usuários.

---

## 📝 Histórias de Usuário

### Épico 1: Autenticação e Gestão de Usuários

#### US-001: Cadastro de Usuário
**Como** um novo usuário  
**Eu quero** criar uma conta  
**Para que** eu possa acessar a plataforma

**Critérios de Aceitação:**
- [ ] Formulário de cadastro com email, senha e confirmação de senha
- [ ] Validação de email único
- [ ] Validação de força de senha (mínimo 8 caracteres)
- [ ] Confirmação de email por link
- [ ] Mensagem de sucesso após cadastro

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-002: Login
**Como** um usuário cadastrado  
**Eu quero** fazer login  
**Para que** eu possa acessar minha conta

**Critérios de Aceitação:**
- [ ] Formulário de login com email e senha
- [ ] Autenticação via JWT
- [ ] Sessão persistente (remember me)
- [ ] Recuperação de senha
- [ ] Tratamento de erros (credenciais inválidas)

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-003: Recuperação de Senha
**Como** um usuário  
**Eu quero** recuperar minha senha  
**Para que** eu possa acessar minha conta se esquecer a senha

**Critérios de Aceitação:**
- [ ] Link "Esqueci minha senha" na tela de login
- [ ] Envio de email com link de redefinição
- [ ] Link válido por 24 horas
- [ ] Formulário de nova senha
- [ ] Confirmação de alteração

**Prioridade:** Média  
**Estimativa:** 2 pontos

---

#### US-004: Perfil do Usuário
**Como** um usuário  
**Eu quero** visualizar e editar meu perfil  
**Para que** eu possa manter minhas informações atualizadas

**Critérios de Aceitação:**
- [ ] Visualização de dados do perfil
- [ ] Edição de nome e email
- [ ] Alteração de senha
- [ ] Upload de foto de perfil (opcional)
- [ ] Salvar alterações

**Prioridade:** Baixa  
**Estimativa:** 2 pontos

---

### Épico 2: Gestão de Empresas

#### US-005: Cadastrar Empresa
**Como** um usuário  
**Eu quero** cadastrar uma empresa  
**Para que** eu possa monitorar convenções aplicáveis

**Critérios de Aceitação:**
- [ ] Formulário com CNPJ, razão social, CNAE, município, UF
- [ ] Validação de CNPJ (formato e dígitos verificadores)
- [ ] Busca automática de dados da Receita Federal (opcional)
- [ ] Validação de CNAE
- [ ] Associação automática de convenções existentes
- [ ] Mensagem de sucesso

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-006: Listar Empresas
**Como** um usuário  
**Eu quero** visualizar minhas empresas cadastradas  
**Para que** eu possa gerenciá-las

**Critérios de Aceitação:**
- [ ] Lista de empresas com informações principais
- [ ] Indicador de número de convenções associadas
- [ ] Filtros por município, CNAE
- [ ] Paginação se houver muitas empresas
- [ ] Link para detalhes de cada empresa

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-007: Visualizar Detalhes da Empresa
**Como** um usuário  
**Eu quero** ver detalhes de uma empresa  
**Para que** eu possa ver convenções associadas e estatísticas

**Critérios de Aceitação:**
- [ ] Exibição de dados completos da empresa
- [ ] Lista de convenções associadas
- [ ] Estatísticas (total de convenções, última atualização)
- [ ] Opção de editar empresa
- [ ] Opção de remover empresa

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-008: Editar Empresa
**Como** um usuário  
**Eu quero** editar dados de uma empresa  
**Para que** eu possa manter informações atualizadas

**Critérios de Aceitação:**
- [ ] Formulário pré-preenchido com dados atuais
- [ ] Validação de campos
- [ ] Reassociação de convenções se CNAE/município mudar
- [ ] Confirmação de alteração

**Prioridade:** Média  
**Estimativa:** 2 pontos

---

#### US-009: Remover Empresa
**Como** um usuário  
**Eu quero** remover uma empresa  
**Para que** eu possa parar de monitorá-la

**Critérios de Aceitação:**
- [ ] Botão de remoção na página de detalhes
- [ ] Confirmação antes de remover
- [ ] Remoção de associações com convenções
- [ ] Manter histórico de notificações (opcional)

**Prioridade:** Média  
**Estimativa:** 2 pontos

---

### Épico 3: Coleta Automática de Dados

#### US-010: Scraper do Mediador MTE
**Como** sistema  
**Eu quero** coletar IDs de instrumentos coletivos do Mediador  
**Para que** eu possa identificar novas convenções

**Critérios de Aceitação:**
- [ ] Acesso ao site do Mediador MTE
- [ ] Extração de IDs de instrumentos coletivos
- [ ] Rate limiting respeitoso (2-5s entre requisições)
- [ ] Tratamento de erros (site indisponível, timeout)
- [ ] Logging de atividades

**Prioridade:** Alta  
**Estimativa:** 8 pontos

---

#### US-011: Extração de Metadados
**Como** sistema  
**Eu quero** extrair metadados de cada convenção  
**Para que** eu possa organizar e indexar convenções

**Critérios de Aceitação:**
- [ ] Extração de título, datas, sindicatos, município, CNAE
- [ ] Validação de campos obrigatórios
- [ ] Normalização de dados (datas, CNPJ, CNAE)
- [ ] Tratamento de campos opcionais
- [ ] Armazenamento de metadados

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-012: Download de Documentos
**Como** sistema  
**Eu quero** baixar documentos (HTML/PDF) das convenções  
**Para que** eu possa processá-los

**Critérios de Aceitação:**
- [ ] Download de HTML e PDF
- [ ] Validação de integridade do arquivo
- [ ] Armazenamento temporário
- [ ] Tratamento de erros de download
- [ ] Retry em caso de falha

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-013: Extração de Texto de HTML
**Como** sistema  
**Eu quero** extrair texto de documentos HTML  
**Para que** eu possa indexar para busca

**Critérios de Aceitação:**
- [ ] Parse de HTML
- [ ] Remoção de tags e scripts
- [ ] Limpeza de espaços em branco
- [ ] Preservação de estrutura básica
- [ ] Armazenamento de texto extraído

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-014: Extração de Texto de PDF Digital
**Como** sistema  
**Eu quero** extrair texto de PDFs digitais  
**Para que** eu possa indexar para busca

**Critérios de Aceitação:**
- [ ] Identificação de PDF digital
- [ ] Extração de texto página por página
- [ ] Preservação de quebras de linha
- [ ] Tratamento de PDFs com proteção
- [ ] Armazenamento de texto extraído

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-015: OCR para PDFs Escaneados
**Como** sistema  
**Eu quero** aplicar OCR em PDFs escaneados  
**Para que** eu possa extrair texto de imagens

**Critérios de Aceitação:**
- [ ] Detecção de PDF escaneado
- [ ] Conversão de PDF em imagens
- [ ] Aplicação de OCR (Tesseract)
- [ ] Pré-processamento de imagens (melhoria de qualidade)
- [ ] Marcação de documentos com baixa confiança

**Prioridade:** Média  
**Estimativa:** 8 pontos

---

#### US-016: Armazenamento de Convenções
**Como** sistema  
**Eu quero** armazenar convenções no banco de dados  
**Para que** eu possa disponibilizá-las aos usuários

**Critérios de Aceitação:**
- [ ] Validação de dados antes de armazenar
- [ ] Verificação de duplicatas (por instrumento_id)
- [ ] Armazenamento de metadados
- [ ] Upload de documento para storage
- [ ] Armazenamento de texto extraído
- [ ] Criação de índices para busca

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-017: Job Agendado de Coleta
**Como** sistema  
**Eu quero** executar coleta automaticamente em intervalos regulares  
**Para que** eu possa manter dados atualizados

**Critérios de Aceitação:**
- [ ] Agendamento de execução (ex: a cada 6 horas)
- [ ] Execução automática do processo de coleta
- [ ] Logging de execuções
- [ ] Notificação em caso de falhas
- [ ] Possibilidade de execução manual

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

### Épico 4: Busca e Visualização

#### US-018: Busca por CNPJ
**Como** um usuário  
**Eu quero** buscar convenções por CNPJ  
**Para que** eu possa encontrar convenções aplicáveis a uma empresa específica

**Critérios de Aceitação:**
- [ ] Campo de busca por CNPJ
- [ ] Validação de formato de CNPJ
- [ ] Busca em metadados e associações
- [ ] Exibição de resultados relevantes
- [ ] Link para detalhes de cada convenção

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-019: Busca por CNAE
**Como** um usuário  
**Eu quero** buscar convenções por CNAE  
**Para que** eu possa encontrar convenções de um setor específico

**Critérios de Aceitação:**
- [ ] Campo de busca por CNAE
- [ ] Validação de formato de CNAE
- [ ] Busca em metadados
- [ ] Exibição de resultados
- [ ] Filtros adicionais (município, período)

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-020: Busca por Município
**Como** um usuário  
**Eu quero** buscar convenções por município  
**Para que** eu possa encontrar convenções de uma localidade específica

**Critérios de Aceitação:**
- [ ] Campo de busca por município
- [ ] Autocomplete de municípios
- [ ] Busca com UF
- [ ] Exibição de resultados
- [ ] Filtros adicionais

**Prioridade:** Alta  
**Estimativa:** 3 pontos

---

#### US-021: Busca por Palavra-chave
**Como** um usuário  
**Eu quero** buscar cláusulas por palavra-chave  
**Para que** eu possa encontrar informações específicas nas convenções

**Critérios de Aceitação:**
- [ ] Campo de busca full-text
- [ ] Busca em texto extraído das convenções
- [ ] Destaque de termos encontrados
- [ ] Exibição de contexto ao redor do termo
- [ ] Filtros por convenção, período, etc.

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-022: Visualizar Convenção
**Como** um usuário  
**Eu quero** visualizar detalhes de uma convenção  
**Para que** eu possa ler o conteúdo completo

**Critérios de Aceitação:**
- [ ] Exibição de metadados completos
- [ ] Visualização de texto extraído formatado
- [ ] Link para documento original
- [ ] Download do documento original
- [ ] Navegação por seções (se estruturado)

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-023: Histórico de Convenções por Empresa
**Como** um usuário  
**Eu quero** visualizar histórico de convenções de uma empresa  
**Para que** eu possa acompanhar evolução ao longo do tempo

**Critérios de Aceitação:**
- [ ] Lista cronológica de convenções
- [ ] Filtros por período
- [ ] Indicador de convenção atual
- [ ] Comparação entre versões (futuro)
- [ ] Exportação de histórico (futuro)

**Prioridade:** Média  
**Estimativa:** 5 pontos

---

### Épico 5: Notificações

#### US-024: Notificação de Nova Convenção
**Como** um usuário  
**Eu quero** receber notificação quando nova convenção aplicável for publicada  
**Para que** eu possa estar sempre atualizado

**Critérios de Aceitação:**
- [ ] Identificação automática de convenções aplicáveis
- [ ] Geração de notificação
- [ ] Envio por email
- [ ] Notificação no dashboard
- [ ] Link direto para convenção

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-025: Preferências de Notificação
**Como** um usuário  
**Eu quero** configurar preferências de notificação  
**Para que** eu possa controlar como e quando recebo alertas

**Critérios de Aceitação:**
- [ ] Configuração de email habilitado/desabilitado
- [ ] Configuração de frequência (imediato, diário, semanal)
- [ ] Seleção de empresas para monitorar
- [ ] Salvar preferências

**Prioridade:** Média  
**Estimativa:** 3 pontos

---

#### US-026: Lista de Notificações
**Como** um usuário  
**Eu quero** visualizar minhas notificações  
**Para que** eu possa acompanhar atualizações

**Critérios de Aceitação:**
- [ ] Lista de notificações não lidas e lidas
- [ ] Marcar como lida
- [ ] Link para convenção relacionada
- [ ] Filtros por tipo, data
- [ ] Paginação

**Prioridade:** Média  
**Estimativa:** 3 pontos

---

### Épico 6: Dashboard

#### US-027: Dashboard Principal
**Como** um usuário  
**Eu quero** visualizar dashboard com visão geral  
**Para que** eu possa ter uma visão consolidada do sistema

**Critérios de Aceitação:**
- [ ] Estatísticas gerais (total de empresas, convenções)
- [ ] Convenções recentes
- [ ] Notificações recentes
- [ ] Ações rápidas (cadastrar empresa, buscar)
- [ ] Gráficos e métricas (futuro)

**Prioridade:** Alta  
**Estimativa:** 5 pontos

---

#### US-028: Dashboard por Empresa
**Como** um usuário  
**Eu quero** visualizar dashboard específico de uma empresa  
**Para que** eu possa ver informações consolidadas sobre convenções aplicáveis

**Critérios de Aceitação:**
- [ ] Informações da empresa
- [ ] Convenções aplicáveis
- [ ] Convenção atual (vigente)
- [ ] Histórico de convenções
- [ ] Estatísticas específicas

**Prioridade:** Média  
**Estimativa:** 5 pontos

---

## 🎯 Priorização do MVP

### Sprint 1 (Fundação)
- US-001: Cadastro de Usuário
- US-002: Login
- US-005: Cadastrar Empresa
- US-006: Listar Empresas
- US-027: Dashboard Principal

### Sprint 2 (Coleta Básica)
- US-010: Scraper do Mediador MTE
- US-011: Extração de Metadados
- US-012: Download de Documentos
- US-013: Extração de Texto de HTML
- US-014: Extração de Texto de PDF Digital
- US-016: Armazenamento de Convenções

### Sprint 3 (Busca e Visualização)
- US-018: Busca por CNPJ
- US-019: Busca por CNAE
- US-020: Busca por Município
- US-022: Visualizar Convenção
- US-007: Visualizar Detalhes da Empresa

### Sprint 4 (Notificações e Melhorias)
- US-017: Job Agendado de Coleta
- US-024: Notificação de Nova Convenção
- US-021: Busca por Palavra-chave
- US-026: Lista de Notificações

### Backlog (Futuro)
- US-003: Recuperação de Senha
- US-004: Perfil do Usuário
- US-008: Editar Empresa
- US-009: Remover Empresa
- US-015: OCR para PDFs Escaneados
- US-023: Histórico de Convenções por Empresa
- US-025: Preferências de Notificação
- US-028: Dashboard por Empresa

---

## 📊 Métricas de Sucesso

- **Cobertura de Coleta:** % de convenções disponíveis no Mediador que foram coletadas
- **Taxa de Sucesso de Extração:** % de documentos com texto extraído com sucesso
- **Tempo de Resposta:** Tempo médio de resposta das buscas
- **Taxa de Notificações:** % de usuários que recebem e abrem notificações
- **Satisfação do Usuário:** NPS ou pesquisa de satisfação

